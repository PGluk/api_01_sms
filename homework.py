import logging
import os
import sys
import time
from logging.handlers import RotatingFileHandler

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

BASE_URL = "https://api.vk.com/method/"
VK_API_VERSION = "5.92"
ACCOUNT_SID = os.getenv("TWILIO_SID")
ACCOUNT_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
NUMBER_FROM = os.getenv('NUMBER_FROM')
NUMBER_TO = os.getenv('NUMBER_TO')

client = Client(ACCOUNT_SID, ACCOUNT_TOKEN)

logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

logger = logging.getLogger('__name__')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    'my_logger.log', maxBytes=50000000, backupCount=5
)
logger.addHandler(handler)


def get_status(user_id):

    status = None
    url = f'{BASE_URL}users.get'
    params = {
        'user_ids': user_id,
        'fields': 'online',
        'v': VK_API_VERSION,
        'access_token': os.getenv('VK_TOKEN')
    }

    try:
        response = requests.post(
            url=url,
            params=params,
            timeout=5,
            ).json()

        if 'online' in response['response'][0]:
            status = response['response'][0]['online']

    except ConnectionError:
        logging.error("Connection error")
    except KeyError:
        logging.error("the key did not found")
        sys.exit()
    return status


def send_sms(sms_text):

    message = client.messages.create(
        body=sms_text,
        from_=NUMBER_FROM,
        to=NUMBER_TO,
    )

    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            send_sms(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
