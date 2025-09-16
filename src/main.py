from fastapi import FastAPI
from src.api.v1.routers import router as v1_routers
from src.core.initializer import AppInitializer

app = FastAPI(
    title="Auth Service",
    summary="Auth Service",
    description="Service for user authentication and authorization",
    docs_url="/",
    contact={
        "name": "Kenzhegulov Arsen",
        "url": "https://github.com/KenArsen/",
        "email": "kenzhegulov.kgz@gmail.com",
    },
)

AppInitializer(app).setup()

app.include_router(v1_routers, prefix="/api")
