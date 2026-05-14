from datetime import date, timedelta
from uuid import UUID
from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.api.loan_policies import repository as loan_policies_repository
from src.api.notifications import service as notification_service
from src.api.copy import repository as copy_repository
from . import dtos, repository


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
# GET ALL PAGINATION
def get_all_pagination(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[dtos.LoanDetailDTO]]:
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


# -----------------------------------------------------------------
# GET USER PAGINATION
def get_all_pagination_by_user(db: Session, user_id: UUID, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[dtos.LoanDetailDTO]]:
  pagination_response = repository.get_all_pagination_by_user(db, user_id, pagination)
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


# -----------------------------------------------------------------
# GET ALL OVERDUE
def get_overdue(db: Session) -> list[dtos.LoanDetailDTO]:
  items = repository.get_overdue(db)
  return [_map_loan_to_detail(item) for item in (items or [])]


# -----------------------------------------------------------------
# CREATE
def create(db: Session, dto: dtos.CreateLoanDTO) -> dtos.LoanDTO:
  policy = loan_policies_repository.get_default_policy(db)
  max_days = int(policy.max_days)

  due_date = date.today() + timedelta(days=max_days)

  loan_dto = dtos.LoanDTO(
    copy_id=dto.copy_id,
    user_id=dto.user_id,
    due_date=due_date,
  )

  created = repository.create(db, loan_dto.model_dump(exclude_none=True))

  if not created or not created.id_loan:
    raise ValueError("Error al crear el préstamo")

  notification_service.notification_for_create_loan_and_send_email(db, created.id_loan)

  return dtos.LoanDTO.model_validate(created)


# -----------------------------------------------------------------
# RETURN BY COPY ID
def return_loan_by_copy_id(db: Session, copy_id: int) -> dtos.LoanDTO | None:
  loan = repository.get_active_loan_by_copy_id(db, copy_id)

  if not loan:
    raise ValueError("No hay préstamo activo para este ejemplar")

  if int(loan.loan_status_id) == 2:
    raise ValueError("Este préstamo ya fue devuelto")

  returned = repository.return_loan(db, loan.id_loan)
  
  copy_repository.update_status(db, loan.copy_id, 1)
  
  notification_service.notification_for_return_loan_and_send_email(db, returned.id_loan)

  return dtos.LoanDTO.model_validate(returned)


# -----------------------------------------------------------------
# UPDATE - EXPIRE OVERDUE
def expire_overdue_loans(db: Session) -> int:
  count = repository.expire_overdue_as_overdue(db)
  
  if count > 0:
    copy_repository.update_all_overdue_status(db)
  
  return count


# -----------------------------------------------------------------
# GET ACTIVE LOAN BY BARCODE
def get_active_by_barcode(db: Session, barcode: str) -> dtos.LoanDetailDTO | None:
  loan = repository.get_active_by_barcode(db, barcode)
  if not loan:
    return None
  return _map_loan_to_detail(loan)