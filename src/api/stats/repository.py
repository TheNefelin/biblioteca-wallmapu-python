from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID


# -----------------------------------------------------------------
# GET ADMIN STATS
async def get_admin_stats(db: AsyncSession) -> dict:
  result = (await db.execute(
    text("""
      SELECT
        (SELECT COUNT(id_reservation) FROM wm_reservations WHERE reservation_status_id = 1) as reservations,
        (SELECT COUNT(id_loan) FROM wm_loans WHERE loan_status_id = 1 OR loan_status_id = 3) as loans,
        (SELECT COUNT(id_book) FROM wm_books) as books,
        (SELECT COUNT(id_user) FROM wm_users) as users,
        (SELECT COUNT(id_news) FROM wm_news) as news;
    """)
  )).fetchone()

  return {
    "reservations": result[0],
    "loans": result[1],
    "books": result[2],
    "users": result[3],
    "news": result[4],
  }


# -----------------------------------------------------------------
# GET USER STATS
async def get_user_stats(db: AsyncSession, user_id: UUID) -> dict:
  result = (await db.execute(
    text("""
      SELECT
        (SELECT COUNT(id_loan) FROM wm_loans WHERE user_id = :uid) as total_borrowed,
        (SELECT COUNT(id_loan) FROM wm_loans WHERE user_id = :uid AND (loan_status_id = 1 OR loan_status_id = 3)) as active_loans,
        (SELECT COUNT(id_loan) FROM wm_loans WHERE user_id = :uid AND loan_status_id = 3) as overdue_loans;
    """),
    {"uid": user_id}
  )).fetchone()

  return {
    "total_borrowed": result[0],
    "active_loans": result[1],
    "overdue_loans": result[2],
  }
