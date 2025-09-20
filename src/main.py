from fastapi import FastAPI

from src.core.startup import AppInitializer


def create_app() -> FastAPI:
    app = FastAPI(
        title="Auth Service",
        summary="Auth Service",
        description="Service for user authentication and authorization",
        docs_url="/docs",
        redoc_url="/redoc",
        contact={
            "name": "Kenzhegulov Arsen",
            "url": "https://github.com/KenArsen/",
            "email": "kenzhegulov.kgz@gmail.com",
        },
    )

    AppInitializer(app).setup()
    return app


app = create_app()
