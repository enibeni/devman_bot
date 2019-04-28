import os
import time
import requests
import telegram
from dotenv import load_dotenv


def send_message_to_telegram(message):
    bot = telegram.Bot(token=os.getenv('TELEGRAM_TOKEN'))
    bot.send_message(chat_id=os.getenv('CHAT_ID'), text=message)


def compose_message(raw_status_data):
    message = f'У вас проверили работу ' \
        f'\"{raw_status_data["new_attempts"][-1]["lesson_title"]}\" \n' \
        f'https://dvmn.org{raw_status_data["new_attempts"][-1]["lesson_url"]}'

    if raw_status_data['new_attempts'][-1]['is_negative']:
        message = f'{message} \n\nК сожалению, в работе нашлись ошибки'
    else:
        message = f'{message} \n\nПреподавателю все понравилось, ' \
            f'можно преступать к следующему уроку!'
    return message


def start_devman_listener(devman_api_key):
    long_polling_timeout = 90
    timestamp = time.time()
    while True:
        try:
            response = requests.get(
                url='https://dvmn.org/api/long_polling/',
                headers={'Authorization': f'Token {devman_api_key}'},
                params={'timestamp': timestamp},
                timeout=long_polling_timeout
            )
            if not response.ok:
                return None
            if response.json()['status'] == 'timeout':
                timestamp = response.json()['timestamp_to_request']
            else:
                message = compose_message(response.json())
                send_message_to_telegram(message)
                timestamp = time.time()
        except requests.exceptions.ReadTimeout:
            pass


if __name__ == '__main__':
    load_dotenv()
    start_devman_listener(os.getenv('DEVMAN_API_KEY'))



