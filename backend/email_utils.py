import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from . import schemas

# Load .env from the same directory as this file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

def send_contact_email(contact_request: schemas.ContactRequestCreate):
    if not all([SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_TO]):
        print("WARNING: SMTP settings are not fully configured in .env file. Email not sent.")
        return

    message = MIMEMultipart("alternative")
    message["Subject"] = f"New Contact Request from {contact_request.name}"
    message["From"] = SMTP_USERNAME
    message["To"] = EMAIL_TO

    text = f"""\
    You have received a new contact request:

    Name: {contact_request.name}
    Email: {contact_request.email}
    Service: {contact_request.service}
    Message:
    {contact_request.message}
    """
    html = f"""\
    <html>
      <body>
        <h3>New Contact Request</h3>
        <ul>
          <li><strong>Name:</strong> {contact_request.name}</li>
          <li><strong>Email:</strong> {contact_request.email}</li>
          <li><strong>Service:</strong> {contact_request.service}</li>
        </ul>
        <h4>Message:</h4>
        <p>{contact_request.message}</p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, EMAIL_TO, message.as_string())
        print("Contact request email sent successfully!")
    except Exception as e:
        print(f"Error: Failed to send email. Exception: {e}")
