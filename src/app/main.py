import datetime

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from loguru import logger
from src.app.db import database

from src.app.api.v1.routers import auth, users, measurements


def get_application():
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]
    fastapi_app = FastAPI(title="Finance Control", version="1.0.0", middleware=middleware)
    return fastapi_app


app = get_application()
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/user", tags=["users"])
app.include_router(measurements.router, prefix="/api/v1/measurement", tags=["measurements"])


@app.on_event("startup")
async def startup_event():
    await database.connect()
    app.state.db = database
    logger.info(f"Server Startup {datetime.datetime.now()}")


@app.on_event("shutdown")
async def shutdown_event():
    if not app.state.db:
        await app.state.db.close()
    logger.info(f"Server Shutdown {datetime.datetime.now()}")
