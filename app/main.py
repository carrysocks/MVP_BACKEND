from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import problem, user

app = FastAPI()

app.include_router(problem.router, tags=["Problems"])
app.include_router(user.router, tags=["Users"])

origins = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)