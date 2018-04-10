import json
import telegram
import requests
import logging
# TODO: Check datetime for updates

from telegram.error import NetworkError, Unauthorized
from time import sleep

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
configuration = json.load(open('notizen.json'))
API_TOKEN = configuration['api_token']
BOT_NAME = configuration['name']
BOT_USERNAME = configuration['username']
SPACEAPI_URL = 'http://club.entropia.de/spaceapi'

update_id = None

def main():
    global update_id
    bot = telegram.Bot(API_TOKEN)

    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    while True:
        try:
            report_status(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            update_id += 1


def is_club_open():
    spaceapi = requests.get(SPACEAPI_URL)
    return spaceapi.json()['open']


def report_status(bot):
    global update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id += 1
        if update.message and update.message.text == 'status':
            if is_club_open():
                update.message.reply_text('Der Club ist offen')
            else:
                update.message.reply_text('Der Club ist zu')


if __name__ == '__main__':
    main()
