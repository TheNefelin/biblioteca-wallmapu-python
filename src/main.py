import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from src.api.auth.routes import router as auth_router
from src.api.users.routes import router as users_router
from src.api.news.routes import router as news_router
from src.api.news_gallery.routes import router as news_gallery_router

app = FastAPI(title="Biblioteca Wallmapu API", description="In development", version="1.0")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
  return FileResponse(os.path.join(static_path, "favicon.ico"))

@app.get("/")
async def root():
  return {
    "status": "Api Running",
    "swagger": "/docs",
  }

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(news_router)
app.include_router(news_gallery_router)
