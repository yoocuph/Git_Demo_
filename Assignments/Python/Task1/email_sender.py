import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import logging
from zenquotes_client import get_daily_quote
from user_manager import list_users
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()  # this loads the secret .env file automatically

# -----------------------------------------------------
# Email settings
# -----------------------------------------------------
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")              
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# -----------------------------------------------------
# Logging setup (logs go to both console + file)
# -----------------------------------------------------
logging.basicConfig(
    filename="email_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -----------------------------------------------------
# Send one email (helper function)
# -----------------------------------------------------
def send_email(to_email, subject, body, retries=3):
    """Send an email with retry attempts."""
    for attempt in range(1, retries + 1):
        try:
            msg = MIMEMultipart()
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)

            logging.info(f"Email sent to {to_email}")
            print(f"Email sent to {to_email}")
            return True

        except Exception as e:
            logging.warning(f"Attempt {attempt}: Failed to send email to {to_email} - {e}")
            print(f"Attempt {attempt}: Failed to send email to {to_email}")
            time.sleep(2)  # wait secs before retrying

    logging.error(f"Giving up on {to_email} after {retries} attempts.")
    return False

# -----------------------------------------------------
# Main function to send quote to all active users
# -----------------------------------------------------
def send_quotes_to_users():
    quote_data = get_daily_quote()
    if not quote_data:
        logging.error("Could not fetch a quote today.")
        print("Could not fetch a quote today.")
        return

    quote, author = quote_data
    logging.info(f"Quote fetched: \"{quote}\" — {author}")

    conn = sqlite3.connect("mindfuel.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, email FROM users WHERE status='active' AND frequency='daily'")
    users = cursor.fetchall()
    conn.close()

    if not users:
        logging.info("No active users found.")
        print("No active users found.")
        return

    success_count = 0
    fail_count = 0

    for name, email in users:
        personalized_msg = (f"Good morning {name},\n\nHere's your motivational quote for today:\n\n\"{quote}\"\n— {author}\n\nStay motivated!\n\nMindFuel Team")

        success = send_email(email, subject="Your Daily MindFuel Quote", body=personalized_msg)
        if success:
            success_count += 1
        else:
            fail_count += 1

    summary = f"Summary: {success_count} emails sent, {fail_count} failed."
    logging.info(summary)
    print(summary)

    # send summary to admin for alert
    admin_email = "aladeyussuf.kofo@gmail.com"
    admin_body = f"Daily Summary:\n\n{summary}\n\nCheck 'email_log.txt' for details."
    send_email(admin_email, "Daily Email Report", admin_body)

    
if __name__ == "__main__":
    send_quotes_to_users()
