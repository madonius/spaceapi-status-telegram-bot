#!/usr/bin/env python3

import json
import telegram
import requests
import logging
import datetime

from telegram.error import NetworkError, Unauthorized
from time import sleep

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
configuration = json.load(open('notizen.json'))
API_TOKEN = configuration['api_token']
BOT_NAME = configuration['name']
BOT_USERNAME = configuration['username']
SPACEAPI_URL = 'http://club.entropia.de/spaceapi'

update_id = None


class SpaceApiStatus(object):
    def __init__(self, spaceapi_url=None):
        self._spaceapi_url = spaceapi_url
        self._spaceapi = self.spaceapi
        self._open = self.open
        self._last_change = self.last_change

    @property
    def spaceapi(self):
        spaceapi = requests.get(self._spaceapi_url)
        return spaceapi.json()

    @property
    def open(self):
        return self._spaceapi['open']

    @property
    def last_change(self):
        last_change = self._spaceapi['state']['lastchange']
        return datetime.datetime.fromtimestamp(last_change)

    @property
    def changed(self, timestamp=None):
        # TODO: Status change detection should be done properly…
        if not timestamp:
            timestamp = datetime.datetime.now()
        seconds_since_change = (timestamp - self._last_change).total_seconds()
        return seconds_since_change < 10.0


class ClubStatusBot(telegram.Bot):
    def __init__(self, token):
        telegram.Bot.__init__(self, token=token)

    def get_update_id(self):
        try:
            return self.get_updates()[0].update_id
        except IndexError:
            return None


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


def report_status(bot):
    global update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id += 1
        if update.message and update.message.text == 'status':
            if clubstatus.open:
                update.message.reply_text('Der Club ist offen')
            else:
                update.message.reply_text('Der Club ist zu')
    clubstatus = SpaceApiStatus(spaceapi_url=SPACEAPI_URL)


if __name__ == '__main__':
    main()
