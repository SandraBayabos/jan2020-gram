import requests
from config import Config
import os

MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
MAILGUN_DOMAIN_NAME = os.getenv('MAILGUN_DOMAIN_NAME')
MAILGUN_BASE_URL = os.getenv('MAILGUN_BASE_URL')


def send_message(amount, image, donator):
    html_message = f"""
    <h1>Congratulations!</h1><br>
    <p>You have just received a donation of ${amount} on the following image:</p>
    <br>
    <p>
    <img width="200px "src="{image}"/>
    </p>
    """

    response = requests.post(
        f"{MAILGUN_BASE_URL}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={"from": f"mailgun@{MAILGUN_DOMAIN_NAME}",
              "to": ["sandra.bayabos@gmail.com"],
              "subject": "This is a piece of shit",
              "text": f"You received a donation from {donator}",
              "html": html_message
              })
    return response
