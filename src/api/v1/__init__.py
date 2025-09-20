from fastapi import APIRouter

from src.api.v1.endpoints.accounts import router as accounts_router

router = APIRouter()

router.include_router(accounts_router)
