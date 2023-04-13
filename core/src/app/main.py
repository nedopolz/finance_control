import asyncio
import datetime

from fastapi import FastAPI
from loguru import logger
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from src.app.api.v1.routers import accounts, categories, operations
from src.app.api.v1.services.db_startup_ini import DBStartUp
from src.app.loaders import database, kafka


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


async def start_kafka_consumer():
    await kafka.consume_user_create()


@app.on_event("startup")
async def startup_event():
    await database.connect()
    app.state.db = database
    await DBStartUp(app.state.db).init_table_defaults()
    logger.info(f"Server Startup {datetime.datetime.now()}")
    asyncio.create_task(start_kafka_consumer())


@app.on_event("shutdown")
async def shutdown_event():
    if not app.state.db:
        await app.state.db.close()
    logger.info(f"Server Shutdown {datetime.datetime.now()}")
