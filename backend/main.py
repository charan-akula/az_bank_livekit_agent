from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.get_token import router as token_router

app = FastAPI(title="LiveKit Token Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(token_router)
