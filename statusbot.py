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
CHANNEL_ID = configuration['telegram_channel_id']
SPACEAPI_URL = 'http://club.entropia.de/spaceapi'



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




def main():

    while True:
        try:
            report_status(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            update_id += 1


def report_status(bot):
    clubstatus = SpaceApiStatus(spaceapi_url=SPACEAPI_URL)


if __name__ == '__main__':
    main()
