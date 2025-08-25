# app/db.py
import os
import asyncpg
from fastapi import FastAPI


DATABASE_URL = os.getenv("DATABASE_URL")


async def init_db(app: FastAPI):
    app.state.db_pool = await asyncpg.create_pool(DATABASE_URL)


async def close_db(app: FastAPI):
    await app.state.db_pool.close()
