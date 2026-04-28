from datetime import date, timedelta
from uuid import UUID
from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.api.loan_policies.repository import get_default_policy
from . import dtos, repository, models


# -----------------------------------------------------------------
# Helper: Map Loan entity -> LoanDetailDTO
def _map_loan_to_detail(loan) -> dtos.LoanDetailDTO:
  return dtos.LoanDetailDTO(
    id_loan=int(loan.id_loan),
    loan_date=loan.loan_date,
    due_date=loan.due_date,
    return_date=loan.return_date,
    loan_status_id=int(loan.loan_status_id),
    loan_status_name=str(loan.loan_status.name),
    user_id=loan.user_id,
    user_name=f"{loan.user.name} {loan.user.lastname or ''}",
    book_id=int(loan.copy.edition.book.id_book) if loan.copy.edition.book else 0,
    book_title=str(loan.copy.edition.book.title) if loan.copy.edition.book else "",
    copy_id=int(loan.copy_id),
    copy_barcode=str(loan.copy.barcode),
    copy_signature=str(loan.copy.signature_topography)
  )


# -----------------------------------------------------------------
# GET ALL PAGINATION (joinedload + mapping plano)
# Combina: 1 query DB + DTO plano con todos los campos
def get_all_pagination(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[dtos.LoanDetailDTO]]:
  try:
    pagination_response = repository.get_all_pagination(db, pagination)
    loans = pagination_response.data or []
    
    data = [_map_loan_to_detail(loan) for loan in loans]

    return PaginationResponseDTO[list[dtos.LoanDetailDTO]](
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
# GET USER PAGINATION
def get_all_pagination_by_user(db: Session, user_id: UUID, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[dtos.LoanDetailDTO]]:
  pagination_response = repository.get_all_pagination_by_user(db, user_id, pagination)
  loans = pagination_response.data or []
  
  data = [_map_loan_to_detail(loan) for loan in loans]

  return PaginationResponseDTO(
    page=pagination_response.page,
    pages=pagination_response.pages,
    items=pagination_response.items,
    data=data,
    next=pagination_response.next,
    prev=pagination_response.prev,
  )


# -----------------------------------------------------------------
# GET ALL OVERDUE
def get_overdue(db: Session) -> list[dtos.LoanDetailDTO]:
  try:
    items = repository.get_overdue(db)
    return [_map_loan_to_detail(item) for item in (items or [])]
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

    if not created or not created.id_loan:
      raise ValueError("Error al crear el préstamo")

    return dtos.LoanDTO.model_validate(created)
  except Exception as e:
    raise e


# -----------------------------------------------------------------
# RETURN BY COPY ID
def return_loan_by_copy_id(db: Session, copy_id: int) -> dtos.LoanDTO | None:
  try:
    loan = repository.get_active_loan_by_copy_id(db, copy_id)
    if not loan:
      raise ValueError("No hay préstamo activo para este exemplar")

    if int(loan.loan_status_id) == 2:
      raise ValueError("Este préstamo ya fue devuelto")

    item = repository.return_loan(db, int(loan.id_loan))
    return dtos.LoanDTO.model_validate(item)
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


# -----------------------------------------------------------------
# GET ACTIVE LOAN BY BARCODE
def get_active_by_barcode(db: Session, barcode: str) -> dtos.LoanDetailDTO | None:
  """
  Busca préstamo activo por barcode del ejemplar.
  Returns loan detail con datos del libro, usuario y copia.
  """
  try:
    loan = repository.get_active_by_barcode(db, barcode)
    if not loan:
      return None
    return _map_loan_to_detail(loan)
  except Exception as e:
    raise e









