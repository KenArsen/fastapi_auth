from fastapi import FastAPI
from src.routers.auth import router as auth_router
from src.core.initializer import AppInitializer

app = FastAPI(summary="Auth Service")

AppInitializer(app).setup()

app.include_router(auth_router)
