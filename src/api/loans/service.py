from datetime import date, timedelta
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.schemas.dtos import CreateLoanDTO, LoanDTO, LoanDetailDTO
from src.api.loan_policies import repository as loan_policies_repository
from src.api.notifications import service as notification_service
from src.api.copy import repository as copy_repository
from . import repository


# -----------------------------------------------------------------
# Helper: Map Loan entity -> LoanDetailDTO
def _map_loan_to_detail(loan) -> LoanDetailDTO:
  return LoanDetailDTO(
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
async def get_all_pagination(db: AsyncSession, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[LoanDetailDTO]]:
  pagination_response = await repository.get_all_pagination(db, pagination)
  loans = pagination_response.data or []

  data = [_map_loan_to_detail(loan) for loan in loans]

  return PaginationResponseDTO[list[LoanDetailDTO]](
    page=pagination_response.page,
    pages=pagination_response.pages,
    items=pagination_response.items,
    data=data,
    next=pagination_response.next,
    prev=pagination_response.prev,
  )


# -----------------------------------------------------------------
# GET USER PAGINATION
async def get_all_pagination_by_user(db: AsyncSession, user_id: UUID, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[LoanDetailDTO]]:
  pagination_response = await repository.get_all_pagination_by_user(db, user_id, pagination)
  loans = pagination_response.data or []

  data = [_map_loan_to_detail(loan) for loan in loans]

  return PaginationResponseDTO[list[LoanDetailDTO]](
    page=pagination_response.page,
    pages=pagination_response.pages,
    items=pagination_response.items,
    data=data,
    next=pagination_response.next,
    prev=pagination_response.prev,
  )


# -----------------------------------------------------------------
# GET ALL OVERDUE
async def get_overdue(db: AsyncSession) -> list[LoanDetailDTO]:
  items = await repository.get_overdue(db)
  return [_map_loan_to_detail(item) for item in (items or [])]


# -----------------------------------------------------------------
# CREATE
async def create(db: AsyncSession, dto: CreateLoanDTO) -> LoanDTO:
  policy = await loan_policies_repository.get_default_policy(db)
  max_days = int(policy.max_days)

  due_date = date.today() + timedelta(days=max_days)

  loan_dto = LoanDTO(
    copy_id=dto.copy_id,
    user_id=dto.user_id,
    due_date=due_date,
  )

  created = await repository.create(db, loan_dto.model_dump(exclude_none=True))

  if not created or not created.id_loan:
    raise ValueError("Error al crear el prÃ©stamo")

  await notification_service.notification_for_create_loan_and_send_email(db, created.id_loan)

  return LoanDTO.model_validate(created)


# -----------------------------------------------------------------
# RETURN BY COPY ID
async def return_loan_by_copy_id(db: AsyncSession, copy_id: int) -> LoanDTO | None:
  loan = await repository.get_active_loan_by_copy_id(db, copy_id)

  if not loan:
    raise ValueError("No hay prÃ©stamo activo para este ejemplar")

  if int(loan.loan_status_id) == 2:
    raise ValueError("Este prÃ©stamo ya fue devuelto")

  returned = await repository.return_loan(db, loan.id_loan, date.today(), 2)

  await copy_repository.update_status(db, loan.copy_id, 1)

  await notification_service.notification_for_return_loan_and_send_email(db, returned.id_loan)

  return LoanDTO.model_validate(returned)


# -----------------------------------------------------------------
# UPDATE - EXPIRE OVERDUE
async def expire_overdue_loans(db: AsyncSession) -> int:
  overdue = await repository.get_overdue_loan_copy_ids(db)
  if not overdue:
    return 0

  loan_ids = [row[0] for row in overdue]
  copy_ids = [row[1] for row in overdue]

  await repository.bulk_update_loan_status(db, loan_ids, 3)
  await repository.bulk_update_copy_status(db, copy_ids, 2)

  return len(loan_ids)


# -----------------------------------------------------------------
# GET ACTIVE LOAN BY BARCODE
async def get_active_by_barcode(db: AsyncSession, barcode: str) -> LoanDetailDTO | None:
  loan = await repository.get_active_by_barcode(db, barcode)
  if not loan:
    return None
  return _map_loan_to_detail(loan)