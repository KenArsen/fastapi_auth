from fastapi import FastAPI
from src.api.v1.routers import router as v1_routers
from src.core.initializer import AppInitializer

app = FastAPI(summary="Auth Service")

AppInitializer(app).setup()

app.include_router(v1_routers, prefix="/api")
