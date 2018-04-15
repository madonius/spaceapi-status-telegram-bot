# SpaceAPI Telegram Status Bot

## Preliminaries
### SpaceAPI
The [SpaceAPI][1] is an schema proposed to announce the status of a hackerspace.
### Telegram Bot
You will need a [Telegram Bot][2]. Most importantle you need an [API-Token][3]
### Channel ID
You will need a channel ID

## Usage
1. Copy the example config file:
   ```bash
   cp config.json.example config.json
   ```
1. Replace the dummy entries in the files with their respective entry
1. Install the dependencies:
      bash
   pip3 install python-telegram-bot requests
1. Run the script:
   ```bash
   ./statusbot.py
   ```


_Finally_: If needed set the debug level in the code to `INFO`


[1]: https://spaceapi.net
[2]: https://core.telegram.org/bots
[3]: https://core.telegram.org/bots#creating-a-new-bot
