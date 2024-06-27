import contextlib
import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .container import Container
from .users import router as users_router
from .settings import ServerSettings


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI):
    container = Container()

    init_resources_coroutine = container.init_resources()
    if init_resources_coroutine:
        await init_resources_coroutine

    yield

    shutdown_resources_coroutine = container.shutdown_resources()
    if shutdown_resources_coroutine:
        await shutdown_resources_coroutine


def build_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    origins = ["http://localhost", "http://localhost:3000"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["POST", ],
        allow_headers=["*"]
    )

    for prefix, router in (("", users_router), ):
        app.include_router(prefix=prefix, router=router)

    return app


def main():
    server_settings = ServerSettings()

    os.system(
        "gunicorn "
        "'auth_backend.api.main:build_app()' "
        "--workers 1 "
        "--worker-class uvicorn.workers.UvicornWorker "
        f"--bind {server_settings.address}"
    )


if __name__ == "__main__":
    main()
