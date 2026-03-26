from sqlalchemy import func, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.api.books.models import Book
from src.api.editorials.models import Editorial
from src.api.authors.models import Author
from src.api.subjects.models import Subject
from src.api.division_regions.models import Region
from src.api.division_provinces.models import Province
from src.api.division_communes.models import Commune
from src.api.news.models import News
from src.api.users.models import User


# -----------------------------------------------------------------
# GET ADMIN STATS 
def get_admin_stats(db: Session) -> dict:
  try:
    result = db.execute(
      text("""
        SELECT
          (SELECT COUNT(id_reservation) FROM wm_reservations WHERE reservation_status_id = 1) as reservations,
          (SELECT COUNT(id_loan) FROM wm_loans WHERE loan_status_id = 1 OR loan_status_id = 3) as loans,
          (SELECT COUNT(id_book) FROM wm_books) as books,
          (SELECT COUNT(id_user) FROM wm_users) as users,
          (SELECT COUNT(id_news) FROM wm_news) as news;
      """)
    ).fetchone()
  
    return {
      "reservations": result[0],
      "loans": result[1],
      "books": result[2],
      "users": result[3],
      "news": result[4],      
    }
  except SQLAlchemyError as e:
    raise e
  
  
# -----------------------------------------------------------------
# GET ALL 
def get_all_admin(db: Session) -> dict:
  try:
    result = db.execute(
      text("""
        SELECT
          (SELECT COUNT(id_user) FROM wm_users) as users,
          (SELECT COUNT(id_news) FROM wm_news) as news,	
          (SELECT COUNT(id_region) FROM wm_regions) as regions,
          (SELECT COUNT(id_province) FROM wm_provinces) as provinces,
          (SELECT COUNT(id_commune) FROM wm_communes) as communes,	
          (SELECT COUNT(id_author) FROM wm_authors) as authors,
          (SELECT COUNT(id_editorial) FROM wm_editorials) as editorials,
          (SELECT COUNT(id_subject) FROM wm_subjects) as subjects,
          (SELECT COUNT(id_book) FROM wm_books) as books;
      """)
    ).fetchone()

    return {
      "users": result[0],
      "news": result[1],
      "regions": result[2],
      "provinces": result[3],
      "communes": result[4],
      "authors": result[5],
      "editorials": result[6],
      "subjects": result[7],
      "books": result[8],
    }
  except SQLAlchemyError as e:
    raise e
  