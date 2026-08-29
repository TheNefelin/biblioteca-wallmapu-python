from dataclasses import dataclass
from datetime import datetime
import httpx
from typing import Optional

from src.core.config import settings


@dataclass
class WelcomeEmailData:
  user_email: str
  user_name: str


@dataclass
class AdminEmailData:
  title: str
  message: str
  is_priority: bool
  user_email: str


@dataclass
class EmailData:
  id: int
  book_title: str
  book_barcode: str
  user_email: str
  expiration_date: Optional[datetime] = None


# -----------------------------------------------------------------
# TEMPLATE: Welcome
async def send_welcome_email(data: WelcomeEmailData) -> Optional[dict]:
  html = f"""
  <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
      <div style="max-width: 600px; margin:0 auto; padding: 20px;">
        <h2 style="color: #4A148C;">¡Bienvenido/a a Biblioteca Wallmapu!</h2>
        <p style="color: #00897B;">Hola {data.user_name},</p>
        <p>Tu cuenta ha sido creada exitosamente. Ya puedes disfrutar de todos los servicios de nuestra biblioteca.</p>
        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
          <p>✅ Reservar libros</p>
          <p>✅ Solicitar préstamos</p>
          <p>✅ Recibir notificaciones en tiempo real</p>
        </div>
        <p style="color: #00897B;">¡Gracias por preferirnos!</p>
      </div>
    </body>
  </html>
  """
  return await send_email(data.user_email, "¡Bienvenido/a a Biblioteca Wallmapu!", html)


# -----------------------------------------------------------------
# TEMPLATE: Admin Message
async def send_admin_email(
  data: AdminEmailData
) -> Optional[dict]:

  priority_banner = ""
  priority_subject_prefix = ""

  if data.is_priority:
    priority_banner = """
      <div style="
        background: #D32F2F;
        color: white;
        padding: 12px;
        border-radius: 5px;
        margin-bottom: 20px;
        text-align: center;
        font-weight: bold;
      ">
        ⚠️ MENSAJE DE ALTA PRIORIDAD ⚠️
      </div>
    """
    priority_subject_prefix = "[IMPORTANTE] "

  html = f"""
  <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
      <div style="max-width: 600px; margin:0 auto; padding: 20px;">
        
        {priority_banner}

        <h2 style="color: {'#D32F2F' if data.is_priority else '#4A148C'};">
          {data.title}
        </h2>

        <div style="
          background: #f8f9fa;
          padding: 15px;
          border-radius: 5px;
          margin: 20px 0;
          border-left: 5px solid {'#D32F2F' if data.is_priority else '#4A148C'};
        ">
          <p style="white-space: pre-line;">
            {data.message}
          </p>
        </div>

        <p style="color: #00897B;">
          Este es un mensaje enviado por la administración de la Biblioteca Wallmapu.
        </p>

      </div>
    </body>
  </html>
  """

  subject = f"{priority_subject_prefix}{data.title}"

  return await send_email(data.user_email, subject, html)


# -----------------------------------------------------------------
# SEND EMAIL - Brevo API
async def send_email(to: str, subject: str, html: str) -> Optional[dict]:
  try:
    async with httpx.AsyncClient(timeout=30) as client:
      response = await client.post(
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
async def send_reservation_created_email(
  data: EmailData
) -> Optional[dict]:
  html = f"""
  <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
      <div style="max-width: 600px; margin:0 auto; padding: 10px;">
        <h2 style="color: #4A148C;">Reserva Creada Exitosamente</h2>
        <p style="color: #00897B;">Tu reserva ha sido registrada en la Biblioteca Wallmapu.</p>

        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
          <p><strong>Reserva #:</strong> {data.id}</p>
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
  return await send_email(data.user_email, f"RESERVA CREADA - #{ data.id }", html)


# -----------------------------------------------------------------
# TEMPLATE: Reservation Cancelled
async def send_reservation_cancelled_email(
  data: EmailData
) -> Optional[dict]:
  html = f"""
  <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
      <div style="max-width: 600px; margin:0 auto; padding: 20px;">
        <h2 style="color: #D81B60;">Reserva Cancelada</h2>
        <p style="color: #00897B;">Tu reserva ha sido cancelada.</p>

        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
          <p><strong>Reserva #:</strong> {data.id}</p>
          <p><strong>Libro:</strong> {data.book_title}</p>
          <p><strong>CodBarra:</strong> {data.book_barcode}</p>          
        </div>

        <p style="color: #00897B;">Si no realizaste esta acción, por favor contacta a la biblioteca.</p>
      </div>
    </body>
  </html>
  """
  return await send_email(data.user_email, f"RESERVA CANCELADA - #{ data.id }", html)


# -----------------------------------------------------------------
# TEMPLATE: Reservation Pickup
async def send_loan_created_email(
  data: EmailData
) -> Optional[dict]:
  html = f"""
  <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
      <div style="max-width: 600px; margin:0 auto; padding: 20px;">
        <h2 style="color: #4A148C;">¡Tu préstamo se ha realizado!</h2>
        <p style="color: #00897B;">El libro ya esta en tus manos, disfrútalo!.</p>

        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
          <p><strong>Préstamo #:</strong> {data.id}</p>
          <p><strong>Libro:</strong> {data.book_title}</p>
          <p><strong>CodBarra:</strong> {data.book_barcode}</p>
          <p><strong>Devolución:</strong> {data.expiration_date.strftime('%d-%m-%Y')}</p>
        </div>

        <p style="color: #00897B;"><strong>Importante:</strong> Debes hacer devolución del libro dentro del plazo fijado.</p>
      </div>
    </body>
  </html>
  """
  return await send_email(data.user_email, f"PRÉSTAMO REALIZADO - #{ data.id }", html)


# -----------------------------------------------------------------
# TEMPLATE: Reservation Returned
async def send_loan_returned_email(
  data: EmailData
) -> Optional[dict]:
  html = f"""
  <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
      <div style="max-width: 600px; margin:0 auto; padding: 20px;">
        <h2 style="color: #4A148C;">¡Tu préstamo ha sido devuelto!</h2>
        <p style="color: #00897B;">El libro ya esta disponible!.</p>

        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
          <p><strong>Préstamo #:</strong> {data.id} devuelto exitosamente.</p>
          <p><strong>Libro:</strong> {data.book_title}</p>
          <p><strong>CodBarra:</strong> {data.book_barcode}</p>
        </div>

        <p style="color: #00897B;"><strong>Importante:</strong> Gracias por preferir Wallmapu de Mesana.</p>
      </div>
    </body>
  </html>
  """
  return await send_email(data.user_email, f"PRÉSTAMO DEVUELTO - #{ data.id }", html)

