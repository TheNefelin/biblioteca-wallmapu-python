from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.api.auth.routes import router as auth_router
from src.api.users.routes import router as users_router

app = FastAPI(title="Wallmapu API", description="In development", version="1.0")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
  allow_credentials=True,
)

@app.get("/")
async def root():
  return {
    "status": "Api Running",
    "swagger": "/docs"
  }

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(auth_router)
app.include_router(users_router)
