from sqlalchemy.orm import Session
from . import dtos, repository, models


def get_all(db: Session) -> list[dtos.LoanPolicyDTO]:
  policies = repository.get_all(db)
  return [dtos.LoanPolicyDTO.model_validate(p) for p in policies]


def get_by_id(db: Session, id: int) -> dtos.LoanPolicyDTO:
  policy = repository.get_by_id(db, id)
  if not policy:
    return None
  return dtos.LoanPolicyDTO.model_validate(policy)


def create(db: Session, dto: dtos.CreateLoanPolicyDTO) -> dtos.LoanPolicyDTO:
  policy = models.LoanPolicy(
    name=dto.name,
    max_books=dto.max_books,
    max_days=dto.max_days,
    fine_per_day=dto.fine_per_day,
    reservation_days=dto.reservation_days
  )
  created = repository.create(db, policy)
  return dtos.LoanPolicyDTO.model_validate(created)


def update(db: Session, id: int, dto: dtos.UpdateLoanPolicyDTO) -> dtos.LoanPolicyDTO:
  updated = repository.update(db, id, dto)
  if not updated:
    return None
  return dtos.LoanPolicyDTO.model_validate(updated)


def delete(db: Session, id: int) -> bool:
  return repository.delete(db, id)
