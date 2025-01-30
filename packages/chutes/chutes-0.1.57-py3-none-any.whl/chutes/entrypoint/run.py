"""
Run a chute, automatically handling encryption/decryption via GraVal.
"""

import asyncio
import sys
import time
import hashlib
import gzip
from loguru import logger
import typer
import pickle
import pybase64 as base64
import orjson as json
from functools import lru_cache
from pydantic import BaseModel
from ipaddress import ip_address
from uvicorn import Config, Server
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from substrateinterface import Keypair, KeypairType
from chutes.entrypoint._shared import load_chute
from chutes.chute import ChutePack
from chutes.util.context import is_local


@lru_cache(maxsize=1)
def miner():
    from graval import Miner

    return Miner()


class FSChallenge(BaseModel):
    filename: str
    length: int
    offset: int


class DevMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        """
        Dev/dummy dispatch.
        """
        args = await request.json() if request.method in ("POST", "PUT", "PATCH") else None
        request.state.decrypted = {
            "args": base64.b64encode(gzip.compress(pickle.dumps([]))).decode(),
            "kwargs": base64.b64encode(gzip.compress(pickle.dumps({"json": args}))).decode(),
        }
        return await call_next(request)


class GraValMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: FastAPI, concurrency: int = 1):
        """
        Initialize a semaphore for concurrency control/limits.
        """
        super().__init__(app)
        self.concurrency = concurrency
        self.rate_limiter = asyncio.Semaphore(concurrency)
        self.lock = asyncio.Lock()

    async def _dispatch(self, request: Request, call_next):
        """
        Transparently handle decryption and verification.
        """
        if request.client.host == "127.0.0.1":
            return await call_next(request)

        # Internal endpoints.
        if request.scope.get("path", "").endswith(("/_alive", "/_metrics")):
            ip = ip_address(request.client.host)
            is_private = (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_multicast
                or ip.is_reserved
                or ip.is_unspecified
            )
            if not is_private:
                return ORJSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "go away (internal)"},
                )
            else:
                return await call_next(request)

        # Verify the signature.
        miner_hotkey = request.headers.get("X-Chutes-Miner")
        validator_hotkey = request.headers.get("X-Chutes-Validator")
        nonce = request.headers.get("X-Chutes-Nonce")
        signature = request.headers.get("X-Chutes-Signature")
        if (
            any(not v for v in [miner_hotkey, validator_hotkey, nonce, signature])
            or validator_hotkey != miner()._validator_ss58
            or miner_hotkey != miner()._miner_ss58
            or int(time.time()) - int(nonce) >= 30
        ):
            logger.warning(f"Missing auth data: {request.headers}")
            return ORJSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "go away (missing)"},
            )
        body_bytes = await request.body() if request.method in ("POST", "PUT", "PATCH") else None
        payload_string = hashlib.sha256(body_bytes).hexdigest() if body_bytes else "chutes"
        signature_string = ":".join(
            [
                miner_hotkey,
                validator_hotkey,
                nonce,
                payload_string,
            ]
        )
        if not miner()._keypair.verify(signature_string, bytes.fromhex(signature)):
            return ORJSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "go away (sig)"},
            )

        # Decrypt the payload.
        is_encrypted = request.headers.get("X-Chutes-Encrypted", "false").lower() == "true"
        request.state.decrypted = None
        if is_encrypted and body_bytes:
            encrypted_body = json.loads(body_bytes)
            required_fields = {"ciphertext", "iv", "length", "device_id", "seed"}
            decrypted_body = {}
            for key in encrypted_body:
                if not all(field in encrypted_body[key] for field in required_fields):
                    logger.error(
                        f"Missing encryption fields: {required_fields - set(encrypted_body[key])}"
                    )
                    return ORJSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={
                            "detail": "Missing one or more required fields for encrypted payloads!"
                        },
                    )
                if encrypted_body[key]["seed"] != miner()._seed:
                    logger.error(
                        f"Expecting seed: {miner()._seed}, received {encrypted_body[key]['seed']}"
                    )
                    return ORJSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={"detail": "Provided seed does not match initialization seed!"},
                    )

                try:
                    # Decrypt the request body.
                    ciphertext = base64.b64decode(encrypted_body[key]["ciphertext"].encode())
                    iv = bytes.fromhex(encrypted_body[key]["iv"])
                    decrypted = miner().decrypt(
                        ciphertext,
                        iv,
                        encrypted_body[key]["length"],
                        encrypted_body[key]["device_id"],
                    )
                    assert decrypted, "Decryption failed!"
                    decrypted_body[key] = decrypted
                except Exception as exc:
                    return ORJSONResponse(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content={"detail": f"Decryption failed: {exc}"},
                    )
            request.state.decrypted = decrypted_body
        elif request.method in ("POST", "PUT", "PATCH"):
            request.state.decrypted = await request.json()

        return await call_next(request)

    async def dispatch(self, request: Request, call_next):
        """
        Rate-limiting wrapper around the actual dispatch function.
        """
        if request.scope.get("path", "").endswith(
            ("/_fs_challenge", "/_alive", "/_metrics", "/_ping", "/_device_challenge")
        ):
            return await self._dispatch(request, call_next)
        async with self.lock:
            if self.rate_limiter.locked():
                return ORJSONResponse(
                    status_code=429,
                    content={
                        "error": "RateLimitExceeded",
                        "detail": f"Max concurrency exceeded: {self.concurrency}, try again later.",
                    },
                )
            await self.rate_limiter.acquire()

        # Handle the rate limit semaphore release properly for streaming responses.
        try:
            response = await self._dispatch(request, call_next)
            if hasattr(response, "body_iterator"):
                original_iterator = response.body_iterator

                async def wrapped_iterator():
                    try:
                        async for chunk in original_iterator:
                            yield chunk
                    finally:
                        self.rate_limiter.release()

                response.body_iterator = wrapped_iterator()
                return response
            return response
        finally:
            if not response or not hasattr(response, "body_iterator"):
                self.rate_limiter.release()


# NOTE: Might want to change the name of this to 'start'.
# So `run` means an easy way to perform inference on a chute (pull the cord :P)
def run_chute(
    chute_ref_str: str = typer.Argument(
        ..., help="chute to run, in the form [module]:[app_name], similar to uvicorn"
    ),
    miner_ss58: str = typer.Option(None, help="miner hotkey ss58 address"),
    validator_ss58: str = typer.Option(None, help="validator hotkey ss58 address"),
    port: int | None = typer.Option(None, help="port to listen on"),
    host: str | None = typer.Option(None, help="host to bind to"),
    graval_seed: int | None = typer.Option(None, help="graval seed for encryption/decryption"),
    debug: bool = typer.Option(False, help="enable debug logging"),
    dev: bool = typer.Option(False, help="dev/local mode"),
):
    """
    Run the chute (uvicorn server).
    """

    async def _run_chute():
        _, chute = load_chute(chute_ref_str=chute_ref_str, config_path=None, debug=debug)
        if is_local():
            logger.error("Cannot run chutes in local context!")
            sys.exit(1)

        # Run the server.
        chute = chute.chute if isinstance(chute, ChutePack) else chute

        # GraVal enabled?
        if dev:
            chute.add_middleware(DevMiddleware)
        else:
            if graval_seed is not None:
                logger.info(f"Initializing graval with {graval_seed=}")
                miner().initialize(graval_seed)
                miner()._seed = graval_seed
            chute.add_middleware(GraValMiddleware, concurrency=chute.concurrency)
            miner()._miner_ss58 = miner_ss58
            miner()._validator_ss58 = validator_ss58
            miner()._keypair = Keypair(ss58_address=validator_ss58, crypto_type=KeypairType.SR25519)

        # Run initialization code.
        await chute.initialize()

        # Metrics endpoint.
        async def _metrics():
            return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

        chute.add_api_route("/_metrics", _metrics, methods=["GET"])
        logger.info("Added liveness endpoint: /_metrics")

        # Device info challenge endpoint.
        async def _device_challenge(request: Request, challenge: str):
            return Response(
                content=miner().process_device_info_challenge(challenge),
                media_type="text/plain",
            )

        chute.add_api_route("/_device_challenge", _device_challenge, methods=["GET"])
        logger.info("Added device challenge endpoint: /_device_challenge")

        # Filesystem challenge endpoint.
        async def _fs_challenge(request: Request, challenge: FSChallenge):
            return Response(
                content=miner().process_filesystem_challenge(
                    filename=challenge.filename,
                    offset=challenge.offset,
                    length=challenge.length,
                ),
                media_type="text/plain",
            )

        chute.add_api_route("/_fs_challenge", _fs_challenge, methods=["POST"])
        logger.info("Added filesystem challenge endpoint: /_fs_challenge")

        config = Config(app=chute, host=host, port=port, limit_concurrency=1000)
        server = Server(config)
        await server.serve()

    asyncio.run(_run_chute())
