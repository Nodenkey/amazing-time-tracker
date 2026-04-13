from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import time_entries


app = FastAPI(title="Amazing Time Tracker API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(time_entries.router, prefix="/api/v1")
