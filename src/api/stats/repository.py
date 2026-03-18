from sqlalchemy import func, select
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
from . import dtos

# -----------------------------------------------------------------
# GET ALL 
def get_all_admin(db: Session):
  try:
    query = db.query(
        select(func.count(User.id_user)).scalar_subquery().label("users"),
        select(func.count(News.id_news)).scalar_subquery().label("news"),
        select(func.count(Region.id_region)).scalar_subquery().label("regions"),
        select(func.count(Province.id_province)).scalar_subquery().label("provinces"),
        select(func.count(Commune.id_commune)).scalar_subquery().label("communes"),
        select(func.count(Author.id_author)).scalar_subquery().label("authors"),
        select(func.count(Editorial.id_editorial)).scalar_subquery().label("editorials"),
        select(func.count(Subject.id_subject)).scalar_subquery().label("subjects"),
        select(func.count(Book.id_book)).scalar_subquery().label("books"),
    )

    result = query.one()

    return dtos.StatusAdminDTO(**result._mapping)
  except SQLAlchemyError as e:
    raise e
  