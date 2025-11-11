#pip install pandas
#pip install requests
#pip install schedule


import requests
# import pandas as pd
# import schedule
# import time

# url = "https://zenquotes.io/api/random" #random quotes
# url2 = "https://zenquotes.io/api/quotes" # quotes
# url3 = "https://zenquotes.io/api/today" #qoute of the day

# response = requests.get(url3)

# # print(response.status_code)
# # print(response.text)
# # print(response.json())

# quotes = response.json() 

# # #print(qoute[0]['q'])
# # #print(qoute[0]['a'])
# # #print(qoute[0]['h'])

# quote = quotes[0]['q']
# author = quotes[0]['a']

# print(f'Here is your motivational quote today: \n "{quote}" \n authored by: {author} \n Stay motivated!')

def get_daily_quote():
    """Fetch me todays quote from ZenQuotes API."""
    url3 = "https://zenquotes.io/api/today" #qoute of the day

    try:
        # Send the request (wait max 5 seconds)
        response = requests.get(url3, timeout=5)

        # Check if response is OK
        if response.status_code != 200:
            print(f"Error: Got status code {response.status_code}")
            return None

        # Convert the response to JSON
        quot = response.json()

        # The API usually returns a list with one quote
        if isinstance(quot, list) and len(quot) > 0:
            quote_obj = quot[0]
        elif isinstance(quot, dict):
            quote_obj = quot
        else:
            print("Error: Unexpected data format.")
            return None

        # Extract the quote and author
        quote = quote_obj.get("q")
        author = quote_obj.get("a")

        if not quote or not author:
            print("Error: Missing quote or author.")
            return None

        # Return the quote and author as a tuple
        return quote, author

    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")
        return None
    except ValueError:
        print("Error: Could not decode JSON.")
        return None


# Run the function to test it
if __name__ == "__main__":
    result = get_daily_quote()
    if result:
        quote, author = result
        print(f'Here is your motivational quote today: \n "{quote}" \n authored by: {author} \n Stay motivated!')
    else:
        print("Failed to get a quote today.")



# for q in quotes[:5]:  # print first 5
#     print(f'"{q["q"]}" — {q["a"]}\n')

# def job():
#     print("Hello World")

# schedule.every().day.at("07:00").do(job)

# while True:
#     schedule.run_pending
#     time.sleep(1)

# import smtplib, ssl
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# #from email.mime.application import MIMEApplication

# my_address = "yoocuph@gmail.com"
# password = "sjnwidnwidwidw"

# s = smtplib.SMTP(host = "smtp.gmail.com", port = 587)
# s.starttls()
# s.login(my_address, password)

# msg = MIMEMultipart()
# msg['From'] = my_address
# msg['To'] = aladeyussuf.kofo@gmail.com
# msg['Subject'] = "Get motivated today. Fuel your mind!"
# message = quote
# msg.attach(MIMEText(message, 'plain'))

# def mailScheduler():
#     print("Sending ...")
#     s.send_message(msg)

# schedule.every().day.at("07:00").do(mailScheduler)

# while True:
#     schedule.run_pending
#     time.sleep(1)