from datetime import date, timedelta
from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.api.copy.models import Copy
from src.api.editions.models import Edition
from src.api.loan_policies.repository import get_default_policy
from . import dtos, repository, models, schema


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(pagination: PaginationRequestDTO, db: Session) -> PaginationResponseDTO[list[schema.LoanDetailDTO]]:
  try:
    pagination_response = repository.get_all_pagination(pagination, db)
    data = [schema.LoanDetailDTO.model_validate(loan) for loan in (pagination_response.data or [])]

    return PaginationResponseDTO(
      page=pagination_response.page,
      pages=pagination_response.pages,
      items=pagination_response.items,
      data=data,
      next=pagination_response.next,
      prev=pagination_response.prev,
    )
  except Exception as e:
    raise e


# -----------------------------------------------------------------
# GET ALL OVERDUE
def get_overdue(db: Session) -> list[dtos.LoanDTO]:
  try:
    items = repository.get_overdue(db)
    return [dtos.LoanDTO.model_validate(item) for item in (items or [])]
  except Exception as e:
    raise e


# -----------------------------------------------------------------
# GET BY ID
def get_by_id(db: Session, id: int) -> dtos.LoanDTO | None:
  try:
    item = repository.get_by_id(db, id)
    if not item:
      return None
    return dtos.LoanDTO.model_validate(item)
  except Exception as e:
    raise e


# -----------------------------------------------------------------
# CREATE
def create(db: Session, dto: dtos.CreateLoanDTO) -> dtos.LoanDTO:
  try:
    policy = get_default_policy(db)
    max_days = int(policy.max_days) if policy and policy.max_days else 14

    loan_date = date.today()
    due_date = loan_date + timedelta(days=max_days)

    loan = models.Loan(
      copy_id=dto.copy_id,
      user_id=dto.user_id,
      loan_date=loan_date,
      due_date=due_date,
      loan_status_id=1
    )

    created = repository.create(db, loan)
    result = get_by_id(db, int(created.id_loan))
    
    if result is None:
      raise ValueError("Error al crear el préstamo")
    
    return result
  except Exception as e:
    raise e


# -----------------------------------------------------------------
# RETURN
def return_loan(db: Session, id: int, dto: dtos.ReturnLoanDTO) -> dtos.LoanDTO | None:
  try:
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
  except Exception as e:
    db.rollback()
    raise e


# -----------------------------------------------------------------
# UPDATE - EXPIRE OVERDUE
def expire_overdue_loans(db: Session) -> int:
  try:
    return repository.expire_overdue_as_overdue(db)
  except Exception as e:
    raise e









