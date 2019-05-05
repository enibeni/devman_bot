import os
import time
import requests
from requests import Response
import telegram
from dotenv import load_dotenv


def send_message_to_telegram(message):
    bot = telegram.Bot(token=os.getenv('TELEGRAM_TOKEN'))
    bot.send_message(chat_id=os.getenv('CHAT_ID'), text=message)


def compose_message(raw_status_data):
    last_attempt_data = raw_status_data["new_attempts"][-1]
    message = f'''У вас проверили работу 
\"{last_attempt_data["lesson_title"]}\"
https://dvmn.org{last_attempt_data["lesson_url"]}'''

    if last_attempt_data['is_negative']:
        message = f'{message} К сожалению, в работе нашлись ошибки'
    else:
        message = f'''{message} Преподавателю все понравилось,  
можно преступать к следующему уроку!'''
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
                print('raise_for_status')
                Response.raise_for_status()
            if response.json()['status'] == 'timeout':
                timestamp = response.json()['timestamp_to_request']
            else:
                message = compose_message(response.json())
                send_message_to_telegram(message)
                timestamp = time.time()
        except requests.exceptions.ReadTimeout:
            pass
        except requests.ConnectionError:
            time.sleep(5)
            timestamp = time.time()
        except telegram.error.NetworkError:
            time.sleep(5)
            timestamp = time.time()


if __name__ == '__main__':
    load_dotenv()
    start_devman_listener(os.getenv('DEVMAN_API_KEY'))



