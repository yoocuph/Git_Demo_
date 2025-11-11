import schedule
import time
from email_sender import send_quotes_to_users

def job():
    print("Running scheduled quote delivery...")
    send_quotes_to_users()
    print("Finished sending today's quotes.\n")

# Schedule it for every day at 7:00 AM
schedule.every().day.at("07:00").do(job)

print("Scheduler started... waiting for 7:00 AM to send emails.")

while True:
    schedule.run_pending()   # checks every second if it's time
    time.sleep(60)           # wait 1 minute before checking again
