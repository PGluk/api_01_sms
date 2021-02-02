import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()


def get_status(user_id):
    URL = 'https://api.vk.com/method/users.get'
    VERSION = "5.92"

    params = {
        'user_ids': user_id,
        'fields': 'online',
        'v': VERSION,
        'access_token': os.getenv('VK_TOKEN')
    }

    response = requests.post(url=URL, params=params).json()['response']
    status = response[0]['online']

    return status


def send_sms(sms_text):
    ACCOUNT_SID = os.getenv("TWILIO_SID")
    ACCOUNT_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    NUMBER_FROM = os.getenv('NUMBER_FROM')
    NUMBER_TO = os.getenv('NUMBER_TO')

    client = Client(ACCOUNT_SID, ACCOUNT_TOKEN)

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
