import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

URL = "https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B07W55DDFB/ref=sr_1_1?qid=1597662463"
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
BUY_PRICE = 200

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36",
    "Accept-Language": "cs-CZ,cs;q=0.9,sk;q=0.8,en;q=0.7,fr;q=0.6",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

response = requests.get(url=URL, headers=headers)

soup = BeautifulSoup(response.content, "html.parser")
price = soup.find("span", class_="a-offscreen").getText()
price = float(price.strip("$"))
name = soup.find("span", id="productTitle").getText().strip()

if price < BUY_PRICE:
    message = f"Subject: Amazon Price Alert!\n\n{name} is now ${price}.\n{URL}"
    message = message.encode("utf-8")  # Solves problem with "UnicodeEncodeError: 'ascii' codec can't encode character '\xe9'"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL,
                            msg=message)
