import requests
from typing import Optional

from src.core.config import settings


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
                "sender": {"email": settings.BREVO_FROM_EMAIL, "name": "Biblioteca Wallmapu"},
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
    to_email: str,
    reservation_id: int,
    book_title: str,
    expiration_date: str
) -> Optional[dict]:
    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin:0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">Reserva Creada Exitosamente</h2>
                <p>Tu reserva ha sido registrada en la Biblioteca Wallmapu.</p>

                <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Reserva #:</strong> {reservation_id}</p>
                    <p><strong>Libro:</strong> {book_title}</p>
                    <p><strong>Vence:</strong> {expiration_date}</p>
                </div>

                <p>Recuerda retirar tu libro antes de la fecha de vencimiento.</p>
                <p>¡Gracias por usar nuestra biblioteca!</p>
            </div>
        </body>
    </html>
    """
    return send_email(to_email, "RESERVA CREADA", html)


# -----------------------------------------------------------------
# TEMPLATE: Reservation Cancelled
def send_reservation_cancelled_email(
    to_email: str,
    reservation_id: int,
    book_title: str
) -> Optional[dict]:
    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin:0 auto; padding: 20px;">
                <h2 style="color: #e74c3c;">Reserva Cancelada</h2>
                <p>Tu reserva ha sido cancelada.</p>

                <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Reserva #:</strong> {reservation_id}</p>
                    <p><strong>Libro:</strong> {book_title}</p>
                </div>

                <p>Si no realizaste esta acción, por favor contacta a la biblioteca.</p>
            </div>
        </body>
    </html>
    """
    return send_email(to_email, "RESERVA CANCELADA", html)


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
