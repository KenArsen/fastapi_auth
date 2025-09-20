from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1 import router as v1_routers
from src.core.config import settings
from src.core.logger import setup_logging


class AppInitializer:
    def __init__(self, app: FastAPI):
        self.app = app

    def setup(self):
        self._setup_cors()
        self._setup_logger()
        self._setup_routers()

    def _setup_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _setup_logger(self):
        setup_logging()

    def _setup_routers(self):
        self.app.include_router(v1_routers, prefix="/api/v1")
