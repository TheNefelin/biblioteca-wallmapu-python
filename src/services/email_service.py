from dataclasses import dataclass
from datetime import datetime
import requests
from typing import Optional

from src.core.config import settings


@dataclass
class email_data_reservation():
  id_reservation: int
  book_title: str
  book_barcode: str
  user_email: str
  expiration_date: Optional[datetime] = None


# -----------------------------------------------------------------
# SEND EMAIL - Brevo API
def send_email(to: str, subject: str, html: str) -> Optional[dict]:
  try:
    response = requests.post(
      "https://api.brevo.com/v3/smtp/email",
      headers={
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json"
      },
      json={
        "sender": {"email": settings.BREVO_FROM_EMAIL, "name": settings.BREVO_FROM_NAME},
        "to": [{"email": to}],
        "subject": subject,
        "htmlContent": html
      }
    )
    return response.json()
  except Exception as e:
    print(f"Error sending email to {to}: {e}")
    return None


# -----------------------------------------------------------------
# TEMPLATE: Reservation Created
def send_reservation_created_email(
  data: email_data_reservation
) -> Optional[dict]:
  html = f"""
  <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
      <div style="max-width: 600px; margin:0 auto; padding: 10px;">
        <h2 style="color: #4A148C;">Reserva Creada Exitosamente</h2>
        <p style="color: #00897B;">Tu reserva ha sido registrada en la Biblioteca Wallmapu.</p>

        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
          <p><strong>Reserva #:</strong> {data.id_reservation}</p>
          <p><strong>Libro:</strong> {data.book_title}</p>
          <p><strong>CodBarra:</strong> {data.book_barcode}</p>
          <p><strong>Vence:</strong> {data.expiration_date.strftime('%d-%m-%Y')}</p>
        </div>

        <p style="color: #00897B;">Recuerda retirar tu libro antes de la fecha de vencimiento.</p>
        <p style="color: #00897B;">¡Gracias por usar nuestra biblioteca!</p>
      </div>
    </body>
  </html>
  """
  return send_email(data.user_email, f"RESERVA CREADA - #{ data.id_reservation }", html)


# -----------------------------------------------------------------
# TEMPLATE: Reservation Cancelled
def send_reservation_cancelled_email(
  data: email_data_reservation
) -> Optional[dict]:
  html = f"""
  <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
      <div style="max-width: 600px; margin:0 auto; padding: 20px;">
        <h2 style="color: #D81B60;">Reserva Cancelada</h2>
        <p style="color: #00897B;">Tu reserva ha sido cancelada.</p>

        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
          <p><strong>Reserva #:</strong> {data.id_reservation}</p>
          <p><strong>Libro:</strong> {data.book_title}</p>
          <p><strong>CodBarra:</strong> {data.book_barcode}</p>          
        </div>

        <p style="color: #00897B;">Si no realizaste esta acción, por favor contacta a la biblioteca.</p>
      </div>
    </body>
  </html>
  """
  return send_email(data.user_email, f"RESERVA CANCELADA - #{ data.id_reservation }", html)


# -----------------------------------------------------------------
# TEMPLATE: Reservation Ready (Pickup)
def send_reservation_ready_email(
  to_email: str,
  reservation_id: int,
  book_title: str
) -> Optional[dict]:
  html = f"""
  <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
      <div style="max-width: 600px; margin:0 auto; padding: 20px;">
        <h2 style="color: #27ae60;">¡Tu reserva está lista!</h2>
        <p>El libro que reservaste está disponible para retirar.</p>

        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
          <p><strong>Reserva #:</strong> {reservation_id}</p>
          <p><strong>Libro:</strong> {book_title}</p>
        </div>

        <p><strong>Importante:</strong> Debes retirar el libro dentro de las próximas 48 horas.</p>
      </div>
    </body>
  </html>
  """
  return send_email(to_email, "RESERVA LISTA", html)
