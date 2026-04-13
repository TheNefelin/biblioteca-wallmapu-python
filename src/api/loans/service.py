from datetime import date, timedelta
from sqlalchemy.orm import Session
from . import dtos, repository, models
from src.api.copy.models import Copy
from src.api.editions.models import Edition
from src.api.loan_policies.repository import get_default_policy


def get_all(db: Session) -> list[dtos.LoanDetailDTO]:
  loans = repository.get_all(db)
  return [_to_detail_dto(db, loan) for loan in loans]


def get_by_id(db: Session, id: int) -> dtos.LoanDetailDTO | None:
  loan = repository.get_by_id(db, id)
  if not loan:
    return None
  return _to_detail_dto(db, loan)


def get_active_by_user_id(db: Session, user_id: str) -> list[dtos.LoanDetailDTO]:
  loans = repository.get_active_by_user_id(db, user_id)
  return [_to_detail_dto(db, loan) for loan in loans]


def get_active_by_book_id(db: Session, book_id: int) -> list[dtos.LoanDetailDTO]:
  loans = repository.get_active_by_book_id(db, book_id)
  return [_to_detail_dto(db, loan) for loan in loans]


def get_overdue(db: Session) -> list[dtos.LoanDetailDTO]:
  loans = repository.get_overdue(db)
  return [_to_detail_dto(db, loan) for loan in loans]


def create(db: Session, dto: dtos.CreateLoanDTO) -> dtos.LoanDetailDTO:
  policy = get_default_policy(db)
  max_days = int(policy.max_days) if policy and policy.max_days else 14

  loan = models.Loan(
    copy_id=dto.copy_id,
    user_id=dto.user_id,
    loan_date=date.today(),
    due_date=dto.due_date or (date.today() + timedelta(days=max_days)),
    loan_status_id=1
  )

  created = repository.create(db, loan)
  result = get_by_id(db, int(created.id_loan))
  if result is None:
    raise ValueError("Error al crear el préstamo")
  return result


def return_loan(db: Session, id: int, dto: dtos.ReturnLoanDTO) -> dtos.LoanDetailDTO | None:
  loan = repository.get_by_id(db, id)
  if not loan:
    return None

  if int(loan.loan_status_id) == 2:
    raise ValueError("Este préstamo ya fue devuelto")

  updated = repository.return_loan(db, id, dto.return_date)

  copy = db.query(Copy).filter(Copy.id_copy == int(loan.copy_id)).first()
  if copy:
    copy.status_id = 1

  db.commit()
  return get_by_id(db, id)


def mark_overdue_loans(db: Session) -> int:
  return repository.mark_overdue_as_overdue(db)


def _to_detail_dto(db: Session, loan: models.Loan) -> dtos.LoanDetailDTO:
  book_id = None
  book_title = None
  copy_barcode = None

  if loan.copy:
    copy_barcode = str(loan.copy.barcode)
    if loan.copy.edition_id:
      edition = db.query(Edition).filter(Edition.id_edition == int(loan.copy.edition_id)).first()
      if edition:
        book_id = int(edition.book_id) if edition.book_id else None
        if edition.book:
          book_title = str(edition.book.title)

  return dtos.LoanDetailDTO(
    id_loan=int(loan.id_loan),
    loan_date=loan.loan_date,
    due_date=loan.due_date,
    return_date=loan.return_date,
    copy_id=int(loan.copy_id),
    user_id=str(loan.user_id),
    loan_status_id=int(loan.loan_status_id),
    loan_status_name=str(loan.status.name) if loan.status else None,
    user_name=str(loan.user.name) if loan.user else None,
    user_lastname=str(loan.user.lastname) if loan.user else None,
    book_id=book_id,
    book_title=book_title,
    copy_barcode=copy_barcode
  )