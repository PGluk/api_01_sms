import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()


def get_status(user_id):
    url = 'https://api.vk.com/method/users.get'
    version = "5.92"
    params = {
        'user_ids': user_id,
        'fields': 'online',
        'v': version,
        'access_token': os.getenv('VK_TOKEN')
    }

    response = requests.post(url=url, params=params).json()['response']
    status = response[0]['online']

    return status


def send_sms(sms_text):
    account_sid = os.getenv("TWILIO_SID")
    account_token = os.getenv("TWILIO_AUTH_TOKEN")
    sms_sender = os.getenv("NUMBER_FROM")
    number_to = os.getenv("NUMBER_to")

    client = Client(account_sid, account_token)

    message = client.messages.create(
        body=sms_text,
        from_=sms_sender,
        to=number_to,
    )

    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            send_sms(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
