from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import health, upload
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI()

app.include_router(health.router)
app.include_router(upload.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)