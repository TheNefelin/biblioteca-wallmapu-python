import os
import time
import uuid
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.responses import FileResponse, JSONResponse

from fastapi_problem.handler import add_exception_handler, new_exception_handler
from rfc9457 import BadRequestProblem, Problem, ServerProblem, UnprocessableProblem

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

from src.core.config import settings
from src.core.limiter import limiter
from src.core.logger import logger, set_request_id

start_time = time.time()

app = FastAPI(title="Biblioteca Wallmapu API", description="In development", version="1.0")

app.add_middleware(
  CORSMiddleware,
  allow_origins=settings.cors_origins_list,
  allow_credentials=True,
  allow_methods=["GET", "POST", "PUT", "DELETE"],
  allow_headers=["*"],
)

# Rate limiting (slowapi) - key por identidad (JWT) o por IP
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


# PROBLEM HANDLERS (respuestas RFC 9457 / Problem Details) --------------
class RequestValidationProblem(UnprocessableProblem):
  type_ = "request-validation-failed"
  title = "Request validation error."

  def __init__(self, errors=None, **kwargs):
    super().__init__(errors=errors, **kwargs)
    self.detail = "; ".join(str(e.get("msg", "")) for e in errors) if errors else self.title


class InternalServerErrorProblem(ServerProblem):
  type_ = "internal-server-error"
  title = "Internal server error."

  def __init__(self, detail=None, **kwargs):
    super().__init__(detail="Internal server error", **kwargs)


class RateLimitProblem(BadRequestProblem):
  type_ = "rate-limit-exceeded"
  title = "Rate limit exceeded."
  status = 429


def rate_limit_handler(eh, request: Request, exc: RateLimitExceeded):
  headers = None
  if hasattr(request.state, "view_rate_limit"):
    response = request.app.state.limiter._inject_headers(
      JSONResponse({}), request.state.view_rate_limit
    )
    headers = dict(response.headers)
  return RateLimitProblem(detail=f"Rate limit exceeded: {exc.detail}", headers=headers)


def log_problem(request: Request, exc: Exception):
  if isinstance(exc, Problem) and exc.status < 500:
    logger.warning("%s: %s", exc.title, exc.detail, extra={
      "props": {"status_code": exc.status}
    })


eh = new_exception_handler(
  logger=logger,
  unhandled_wrappers={
    "422": RequestValidationProblem,
    "500": InternalServerErrorProblem,
  },
  handlers={RateLimitExceeded: rate_limit_handler},
  pre_hooks=[log_problem],
)
add_exception_handler(app, eh)
app.add_exception_handler(RateLimitExceeded, eh)


# Logging JSON por petición: asigna un request_id y registra cada request
@app.middleware("http")
async def log_requests(request: Request, call_next):
  request_id = str(uuid.uuid4())
  set_request_id(request_id)
  start = time.time()
  response = await call_next(request)
  logger.info("%s %s", request.method, request.url.path, extra={
    "props": {
      "request_id": request_id,
      "method": request.method,
      "path": request.url.path,
      "status_code": response.status_code,
      "duration_ms": round((time.time() - start) * 1000, 2),
    }
  })
  return response

BASE_DIR = os.getcwd()  # raíz del proyecto
STATIC_PATH = os.path.join(BASE_DIR, "static") 

app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
  return FileResponse(os.path.join(STATIC_PATH, "favicon.ico"))

#health
@app.get("/")
async def root():
  return {
    "status": "Api Running",
    "swagger": "/docs",
    "version": "1.0.231",
    "uptime_seconds": round(time.time() - start_time, 2),
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
