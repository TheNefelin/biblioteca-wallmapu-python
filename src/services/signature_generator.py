import re
from sqlalchemy.orm import Session

from src.api.editions.models import Edition


def calculate_cutter_from_isbn(isbn: str) -> str:
    digits = re.sub(r'[^0-9]', '', isbn)
    
    if len(digits) < 4:
        return f"X{digits.zfill(3)}"
    
    numbers_part = ""
    
    if digits.startswith('978'):
        numbers_part = digits[3:-1]
    else:
        numbers_part = digits[:-1]
    
    if len(numbers_part) < 3:
        numbers_part = numbers_part.zfill(3)
    
    last_three = numbers_part[-3:]
    
    cutter = f"C{last_three}"
    
    return cutter


def count_copies_by_edition(db: Session, edition_id: int) -> int:
    from src.api.copy.models import Copy
    count = db.query(Copy).filter(Copy.edition_id == edition_id).count()
    return count


def generate_signature_topography(db: Session, edition_id: int) -> str:
    edition = db.query(Edition).filter(Edition.id_edition == edition_id).first()
    
    if not edition:
        raise ValueError(f"Edición {edition_id} no encontrada")
    
    genre_id = edition.book.genre_id
    publication_year = edition.publication_year
    
    isbn = edition.isbn
    cutter = calculate_cutter_from_isbn(isbn)
    
    copy_number = count_copies_by_edition(db, edition_id) + 1
    
    signature = f"{genre_id}-{cutter}-{publication_year}-{copy_number:03d}".upper()
    
    return signature


def generate_barcode(db: Session, edition_id: int) -> str:
    return generate_signature_topography(db, edition_id)
