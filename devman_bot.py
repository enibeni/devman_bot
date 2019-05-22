import os
import time
import requests
import telegram
from dotenv import load_dotenv
import logging
from logs_handler import MyLogsHandler


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
    logger.info('Бот запущен')
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
            review_data = response.json()
            if not response.ok:
                response.raise_for_status()
            elif review_data['status'] == 'timeout':
                timestamp = review_data['timestamp_to_request']
            else:
                message = compose_message(review_data)
                send_message_to_telegram(message)
                timestamp = review_data['last_attempt_timestamp']
                logger.info('Отправлено сообщение об изменении статуса проверки работы')
        except requests.exceptions.ReadTimeout:
            pass
        except requests.ConnectionError:
            logger.error('Бот упал с ошибкой:')
            logger.exception('ConnectionError exception')
            time.sleep(5)
        except telegram.error.NetworkError:
            logger.error('Бот упал с ошибкой:')
            logger.exception('Telegram NetworkError exception')
            time.sleep(5)


if __name__ == '__main__':
    load_dotenv()
    logger = logging.getLogger("Название логера")
    logger.setLevel(logging.DEBUG)
    handler = MyLogsHandler()
    logger.addHandler(handler)

    start_devman_listener(os.getenv('DEVMAN_API_KEY'))



