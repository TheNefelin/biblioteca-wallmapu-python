import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from src.api.stats.routes import router as stats_router
from src.api.auth.routes import router as auth_router
from src.api.division_regions.routes import router as regions_router
from src.api.division_provinces.routes import router as provinces_router
from src.api.division_communes.routes import router as communes_router
from src.api.user_role.routes import router as users_role_router
from src.api.user_status.routes import router as users_status_router
from src.api.users.routes import router as users_router
from src.api.news.routes import router as news_router
from src.api.news_gallery.routes import router as news_gallery_router
from src.api.genres.routes import router as genres_router
from src.api.authors.routes import router as authors_router
from src.api.book_authors.routes import router as book_authors_router
from src.api.subjects.routes import router as subjects_router
from src.api.book_subjects.routes import router as book_subjects_router
from src.api.books.routes import router as books_router
from src.api.editorials.routes import router as editorials_router
from src.api.editions.routes import router as editions_router
from src.api.edition_image.routes import router as edition_image_router
from src.api.format.routes import router as format_router
from src.api.edition_format.routes import router as edition_format_router
from src.api.copy.routes import router as copy_router
from src.api.copy_status.routes import router as copy_status_router
from src.api.reservation_status.routes import router as reservation_status_router
from src.api.reservations.routes import router as reservations_router
from src.api.loans.routes import router as loans_router
from src.api.loan_policies.routes import router as loan_policies_router
from src.api.loan_status.routes import router as loan_status_router
from src.api.notifications.routes import router as notifications_router

app = FastAPI(title="Biblioteca Wallmapu API", description="In development", version="1.0")

app.add_middleware(
  CORSMiddleware,
  allow_origins=[
    #"http://localhost:4200",
    "https://biblioteca-wallmapu-angular.vercel.app",
    "https://www.wallmapumesana.cl",
    "https://wallmapumesana.cl",
  ],
  allow_credentials=True,
  allow_methods=["GET", "POST", "PUT", "DELETE"],
  allow_headers=["*"],
)

BASE_DIR = os.getcwd()  # raíz del proyecto
STATIC_PATH = os.path.join(BASE_DIR, "static") 

app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
  return FileResponse(os.path.join(STATIC_PATH, "favicon.ico"))

@app.get("/")
async def root():
  return {
    "status": "Api Running",
    "swagger": "/docs",
    "version": "231", 
  }

app.include_router(stats_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(regions_router, prefix="/api")
app.include_router(provinces_router, prefix="/api")
app.include_router(communes_router, prefix="/api")
app.include_router(users_role_router, prefix="/api")
app.include_router(users_status_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(news_router, prefix="/api")
app.include_router(news_gallery_router, prefix="/api")
app.include_router(genres_router, prefix="/api")
app.include_router(authors_router, prefix="/api")
app.include_router(book_authors_router, prefix="/api")
app.include_router(subjects_router, prefix="/api")
app.include_router(book_subjects_router, prefix="/api")
app.include_router(books_router, prefix="/api")
app.include_router(editorials_router, prefix="/api")
app.include_router(editions_router, prefix="/api")
app.include_router(edition_image_router, prefix="/api")
app.include_router(format_router, prefix="/api")
app.include_router(edition_format_router, prefix="/api")
app.include_router(copy_router, prefix="/api")
app.include_router(copy_status_router, prefix="/api")
app.include_router(reservations_router, prefix="/api")
app.include_router(reservation_status_router, prefix="/api")
app.include_router(loans_router, prefix="/api")
app.include_router(loan_status_router, prefix="/api")
app.include_router(loan_policies_router, prefix="/api")
app.include_router(notifications_router, prefix="/api")

