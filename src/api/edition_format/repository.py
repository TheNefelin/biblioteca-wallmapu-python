from sqlalchemy.orm import Session

from . import models


# -----------------------------------------------------------------
# UPDATE
def update(db: Session, id_edition: int, format_ids: list[int]) -> list[models.EditionFormat]:
  db.query(models.EditionFormat).filter(
    models.EditionFormat.id_edition == id_edition
  ).delete(synchronize_session=False)

  relations = [
    models.EditionFormat(id_edition=id_edition, id_format=fid)
    for fid in format_ids
  ]

  if relations:
    db.add_all(relations)

  db.commit()

  return relations


# -----------------------------------------------------------------
# DELETE
def delete(db: Session, id_edition: int, id_format: int) -> bool:
  relation = db.get(
    models.EditionFormat,
    (id_edition, id_format)
  )

  if not relation:
    return False

  db.delete(relation)
  db.commit()

  return True


# -----------------------------------------------------------------
# GET BY EDITION
def get_by_edition(db: Session, id_edition: int) -> list[models.EditionFormat]:
  return (
    db.query(models.EditionFormat)
    .filter(models.EditionFormat.id_edition == id_edition)
    .all()
  )


# -----------------------------------------------------------------
# DELETE BY ID EDITION
def delete_by_edition(db: Session, id_edition: int) -> bool:
  rows_deleted = (
    db.query(models.EditionFormat)
    .filter(models.EditionFormat.id_edition == id_edition)
    .delete(synchronize_session=False)
  )

  db.commit()

  return rows_deleted > 0
