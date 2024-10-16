import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environments variables from .env file
load_dotenv()


def create_message(subject, body, from_email, to_email):
    """
    Creates an email message with the given subject, body, from and to email addresses.
    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    return msg


def send_email(server, msg, from_email, to_email):
    """
    Sends an email message using the provided SMTP server.
    """
    server.sendmail(from_email, to_email, msg.as_string())
    print(f"Email Sent. To: {to_email} From: {from_email} Subject: {msg['Subject']}")


def login_to_smtp():
    """
    Logs in to the SMTP server using credentials from environments variables.
    Returns an authenticated SMTP server object.
    """
    from_email = os.getenv('EMAIL_ADDRESS')
    app_password = os.getenv('EMAIL_PASSWORD')
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(from_email, app_password)
    return server


def main(subject, body, to_email):
    """
    Main function to create an email message, login to the SMTP server, and send the email.
    """
    from_email = os.getenv('EMAIL_ADDRESS')
    msg = create_message(subject, body, from_email, to_email)
    server = login_to_smtp()
    send_email(server, msg, from_email, to_email)
    server.quit()
