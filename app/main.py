import aioboto3
from fastapi import FastAPI

from app.api.routes.router import grouping_router
from app.core import config


def get_application() -> FastAPI:
    application = FastAPI(
        debug=config.DEBUG,
        title="MA",
        description="MA test task",
        version=config.VERSION,
        redirect_slashes=True
    )

    application.include_router(grouping_router)

    return application


app = get_application()
