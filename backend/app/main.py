from fastapi import FastAPI

from contextlib import asynccontextmanager
from app.core.database import init_db
from app.api import endpoints

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="AI Destekli İş/Staj Uyum Analizi API", lifespan=lifespan)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(endpoints.router)

@app.get("/")
async def root():
    return FileResponse("app/static/index.html")
