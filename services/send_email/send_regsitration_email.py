import os
import requests


def send_simple_message(to, subject, body):
    domain = os.getenv('MAILGUN_DOMAIN')
    api_key = os.getenv('MAILGUN_API_KEY')
    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={"from": "Flask Docker <mailgun@{domain}>",
              "to": [to],
              "subject": subject,
              "text": body})