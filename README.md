# Devman bot

Stay informed about your Devman work check status with the combination of this script and your telegram bot

### How to install

To use this script you should provide certain keys as environment variables in the .env file.
The keys you need to provide:
DEVMAN_API_KEY - provided in devman api docs https://dvmn.org/api/docs/
TELEGRAM_TOKEN - your telegram bot api key
TELEGRAM_TOKEN_LOGGER - your telegram bot api key for logging
CHAT_ID - your telegram chat id provided via @userinfobot bot

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

You will need two telegram bots for this script. One for notification about work check status
and another one for logging. Find out how to create them on telegram docs https://core.telegram.org/bots

# Quickstart

```bash
$ python3 devman_bot.py
```


### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).