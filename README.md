# Bibabot
This is bibabot, a Telegram bot running in Azure Functions to post stuff about your ESPN Fantasy NBA league into your group chat.

Features include:
* Posting whenever a transaction has happened (Player dropped, FA acquired, Trade, ...)
* Posting regular Power Rankings

## Setup
This project uses the [espn_api](https://github.com/cwendt94/espn-api) Python package. To get the ESPN S2 and SWID follow the guidelines posted in [espn_api](https://github.com/cwendt94/espn-api/discussions/150).

Find the docs on how to create a Telegram Bot here: [Telegram Bot Setup](https://core.telegram.org/bots#3-how-do-i-create-a-bot).

The code is intended to run as an Azure Function. To get started, follow these steps:
* [Create an Azure Function with Python](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python)
* [Azure Functions Python developer guide](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python)

Your Azure Function should provide the following Env variables:
* `BIBA_TELEGRAM_BOT_TOKEN`: Token of your Telegram bot
* `BIBA_TELEGRAM_CHANNEL`: Channel ID to post into
* `BIBA_ESPN_LEAGUEID`: The league ID of your ESPN Fantasy league
* `BIBA_ESPN_LEAGUE_YEAR`: The year of your ESPN Fantasy league
* `BIBA_ESPN_S2`: The S2 value of your ESPN Fantasy league
* `BIBA_ESPN_SWID`: The SWID value of your ESPN Fantasy league

## Dev Setup
The unittests load the local.settings.json to run locally. I recommend using the channel-id of a private chat with your bot so running local test won't spam your league channel.
