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

last_club_status = None


class SpaceApiStatus(object):
    """
    An object collecting the entropia status from the spaceapi
    """
    def __init__(self, spaceapi_url=None):
        """
        :param spaceapi_url: the URL where the spaceapi JSON is located
        :type spaceapi_url str
        """
        self._spaceapi_url = spaceapi_url
        self._spaceapi = self.spaceapi
        self._open = self.open
        self._last_change = self.last_change

    @property
    def spaceapi(self):
        """
        Retrieve the api's contents
        :return: the api's contents
        :rtype: dict
        """
        spaceapi = requests.get(self._spaceapi_url)
        return spaceapi.json()

    @property
    def open(self):
        """
        The space's status
        :return: the spaces's status
        :rtype: bool
        """
        return self._spaceapi['open']

    @property
    def last_change(self):
        """
        The status's last change timestamp
        :return: Date of the last statuschange
        :rtype: datetime.datetime
        """
        last_change = self._spaceapi['state']['lastchange']
        return datetime.datetime.fromtimestamp(last_change)

    @property
    def changed(self, timestamp=None):
        """
        Check if the status has changed
        :param timestamp: The timestamp since when the last check
        :type timestamp: datetime.datetime
        :return: whethes the status has changed since the timestamp
        :rtype: bool
        """
        # TODO: Status change detection should be done properly…
        if not timestamp:
            timestamp = datetime.datetime.now()
        seconds_since_change = (timestamp - self._last_change).total_seconds()
        return seconds_since_change < 10.0


def main():
    global last_club_status

    bot = telegram.Bot(API_TOKEN)
    while True:
        try:
            report_status(bot)
        except NetworkError:
            sleep(1)


def report_status(bot):
    """
    Report the spaceapi state to the Telegram channel
    :param bot: Telegram Bot connection
    :type bot: telegram.Bot
    :return: None
    :rtype: None
    """
    global last_club_status

    message = None
    clubstatus = SpaceApiStatus(spaceapi_url=SPACEAPI_URL)
    if clubstatus.open != last_club_status:
        last_club_status = clubstatus.open
        if clubstatus.open:
            message = 'Der Club ist offen'
        else:
            message = 'Der Club ist zu'

        bot.send_message(CHANNEL_ID, message)


if __name__ == '__main__':
    main()
