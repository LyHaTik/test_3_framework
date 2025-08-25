from fastapi import FastAPI
from app.db import init_db, close_db
from app.routes import router


app = FastAPI(title="Tasks API")
app.include_router(router)


@app.on_event("startup")
async def on_startup():
    await init_db(app)


@app.on_event("shutdown")
async def on_shutdown():
    await close_db(app)
