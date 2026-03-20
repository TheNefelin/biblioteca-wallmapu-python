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
# GET ALL 
def get_all_admin(db: Session) -> dict:
  try:
    result = db.execute(
      text("""
        SELECT 
          (SELECT COUNT(*) FROM users) AS users,
          (SELECT COUNT(*) FROM news) AS news,
          (SELECT COUNT(*) FROM division_regions) AS regions,
          (SELECT COUNT(*) FROM division_provinces) AS provinces,
          (SELECT COUNT(*) FROM division_communes) AS communes,
          (SELECT COUNT(*) FROM authors) AS authors,
          (SELECT COUNT(*) FROM editorials) AS editorials,
          (SELECT COUNT(*) FROM subjects) AS subjects,
          (SELECT COUNT(*) FROM books) AS books
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
  