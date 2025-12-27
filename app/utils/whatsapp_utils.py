from twilio.rest import Client
import os

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)


def send_whatsapp_confirmation(phone: str, name: str, event: str, category: str, team: str | None):
    message_body = f"""
🎉 *Umang 2025 Registration Confirmed!*

👤 Name: {name}
🏅 Event: {event}
📂 Category: {category}
👥 Team / Pair: {team if team else "Solo"}

📍This website has been designed and developed by Shubham Karn, CSE (IoT), 2024 batch, Government Engineering College, Gopalganj.
 phone number: +919366923264
Best wishes,
*Umang 2025 Team*
"""

    client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        to=f"whatsapp:+91{phone}",
        body=message_body
    )
