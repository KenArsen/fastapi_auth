from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.logger import setup_logging


class AppInitializer:
    def __init__(self, app: FastAPI):
        self.app = app

    def setup(self):
        self._setup_cors()
        setup_logging()

    def _setup_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @staticmethod
    def _setup_logger():
        setup_logging()
