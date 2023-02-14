import requests
from bs4 import BeautifulSoup
import smtplib
import datetime
import pytz
import time

# Set the URL of the product page to scrape
url = 'https://shop.mango.com/us/men/coats-coats/wool-overcoat_37084770.html'

# Set the sender and recipient email addresses and login credentials
sender_email = 'xxx'
sender_password = 'xxx'
recipient_email = 'xxx'

# Define a function to check the price of the product
def check_price():
    # Send a GET request to the product page
    response = requests.get(url)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the price element on the page
   #  price_element = soup.find('span', {'class': 'product-features-prices'})

    # Extract the price value from the element
    # price_text = price_element.text
    price_text = soup.find(string=lambda t: '$' in t)
    price = float(price_text.replace('$', '').replace(',', ''))

    # Send an email to the recipient with the current price
    message = 'The price of the product is now ${:.2f}.'.format(price)
    send_email(message)

# Define a function to send an email
def send_email(message):
    # Set up the SMTP server and login with the sender email credentials
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # Compose the email message and send it to the recipient
    subject = 'Product Price Alert'
    body = message
    email_text = 'Subject: {}\n\n{}'.format(subject, body)
    server.sendmail(sender_email, recipient_email, email_text)

    # Close the SMTP server connection
    server.quit()

# Set up a loop to check the price and send an email at 11:30 PM CST every day
while True:
    # Get the current time in the Central Time Zone
    central = pytz.timezone('US/Central')
    now = datetime.datetime.now(central)

    # Check if the current time is 11:30 PM CST
    if now.hour == 23 and now.minute == 38:
        check_price()
        time.sleep(60)  # Wait for 1 minute before checking again
    else:
        time.sleep(30)  # Wait for 30 seconds before checking again
