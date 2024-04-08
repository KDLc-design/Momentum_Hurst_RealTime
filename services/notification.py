# Function to send an email notification
import smtplib
from email.mime.text import MIMEText

def send_email_notification(subject, body):
    sender_email = "xyz@gmail.com"  # Replace with your email address
    receiver_email = "abc@gmail.com"  # Replace with the recipient's email address
    smtp_server = "smtp.gmail.com"  # Replace with the SMTP server address
    smtp_port = 587  # Replace with the SMTP server port
    smtp_username = "xyz@gmail.com"  # Replace with your SMTP username (if required)
    smtp_password = "12345678910"  # Replace with your SMTP password (if required)

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable TLS encryption
            server.login(smtp_username, smtp_password)  # Login to the SMTP server (if required)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(f"Failed to send email notification. Error: {e}")