from src.api.v1.endpoints.auth import router as auth_router
from fastapi import APIRouter

router = APIRouter(prefix="/v1")
router.include_router(auth_router)
