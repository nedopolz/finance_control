import datetime

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from loguru import logger

from src.app.api.v1.services.db_startup_ini import DBStartUp
from src.app.db import database

from src.app.api.v1.routers import accounts, categories, operations


def get_application():
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]
    fastapi_app = FastAPI(
        title="Finance Control", version="1.0.0", middleware=middleware
    )
    return fastapi_app


app = get_application()
app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(operations.router, prefix="/operations", tags=["operations"])


@app.on_event("startup")
async def startup_event():
    await database.connect()
    app.state.db = database
    await DBStartUp(app.state.db).init_table_defaults()
    logger.info(f"Server Startup {datetime.datetime.now()}")


@app.on_event("shutdown")
async def shutdown_event():
    if not app.state.db:
        await app.state.db.close()
    logger.info(f"Server Shutdown {datetime.datetime.now()}")
