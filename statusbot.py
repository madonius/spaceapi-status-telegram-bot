#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A script that executes a telegram Bot that notifies users in a chat/channel of a status change in the hackerspace
"""
__author__ = "Emmanouil 'madonius' Kampitakis"
__copyright__ = "Copyright 2018"
__credits__ = ["Emmanouil Kampitakis"]
__license__ = "MIT"
__version__ = "0.1-beta"
__maintainer__ = "Emmanouil Kampitakis"
__email__ = "info+git@kampitakis.de"
__status__ = "Beta"

import json
import telegram
import requests
import logging
import datetime
import random

from telegram.error import NetworkError, Unauthorized
from time import sleep

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
configuration    = json.load(open('config.json'))
open_messages    = configuration.get("open_messages")
cloesed_messages = configuration.get("closed_messages")
API_TOKEN = configuration['api_token']
BOT_NAME = configuration['name']
BOT_USERNAME = configuration['username']
CHANNEL_ID = configuration['telegram_channel_id']
SPACEAPI_URL = configuration['spaceapi_url']


class SpaceApiStatus(object):
    """
    An object collecting the entropia status from the spaceapi
    """
    def __init__(self, spaceapi_url=None, last_state=None):
        """
        :param spaceapi_url: the URL where the spaceapi JSON is located
        :type spaceapi_url str
        """
        self.last_state = last_state
        self._spaceapi_url = spaceapi_url
        self._spaceapi = None
        self._open = None
        self._last_change = None
        self.update()

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
    def changed_since(self, timestamp=None):
        """
        Check if the status has changed
        :param timestamp: The timestamp since when the last check
        :type timestamp: datetime.datetime
        :return: whethes the status has changed since the timestamp
        :rtype: bool
        """
        # TODO: Status change detection should be done properly
        if not timestamp:
            timestamp = datetime.datetime.now()
        seconds_since_change = (timestamp - self._last_change).total_seconds()
        return seconds_since_change < 10.0

    def changed_from(self, last_state=None):
        """
        Check if the last state is the current one
        :param last_state: the last state of the space
        :type last_state: bool
        :return: Whether the state has chenged
        :rtype: bool
        """
        self.update()
        if type(self.last_state) == bool:
            last_state = self.last_state

        if not type(last_state) == bool:
            return True

        if last_state == self.open:
            return False
        else:
            return True

    def hold_state(self):
        """
        Hold that state
        :return: None
        """

        self.last_state = self.open

    def update(self):
        """
        Update the object with the space api
        :return: None
        """
        self._spaceapi = self.spaceapi
        self._open = self.open
        self._last_change = self.last_change


def main():

    bot = telegram.Bot(API_TOKEN)
    clubstatus = SpaceApiStatus(spaceapi_url=SPACEAPI_URL)
    while True:
        try:
            report_status(bot, clubstatus)
        except NetworkError:
            sleep(1)


def report_status(bot, clubstatus):
    """
    Report the spaceapi state to the Telegram channel
    :param bot: Telegram Bot connection
    :type bot: telegram.Bot
    :param clubstatus: SpaceApi instance
    :type clubstatus: SpaceApiStatus
    :return: None
    :rtype: None
    """

    if clubstatus.changed_from():
        if not clubstatus.last_state:
            bot.send_message(CHANNEL_ID, "Good day! I was just started.\nReady to report!\n:-)")

        if clubstatus.open:
            message = random.choice(open_messages)
        else:
            message = random.choice(closed_messages)

        bot.send_message(CHANNEL_ID, message)
        clubstatus.hold_state()


if __name__ == '__main__':
    main()
