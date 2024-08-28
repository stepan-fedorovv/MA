from fastapi import APIRouter

from .files import router as routes

v1_router = APIRouter()

v1_router.include_router(routes, tags=["example"], prefix="/files")
