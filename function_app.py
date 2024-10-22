
import os
import logging
from pprint import pformat

import azure.functions as func
from espn_api.basketball import League #Ref: https://github.com/cwendt94/espn-api/wiki/League-Class-Basketball

from bibabot.BotHandler import BotHandler
from bibabot.BibaCommand import BibaCommand
from bibabot.RecentActivityCommand import RecentActivityCommand
from bibabot.TelegramBot import TelegramBot

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
TIMER_DURATION_SECS = 1 * 60 * 60 # 1 hour

def check_environment_variables():
    if not os.environ.get("BIBA_TELEGRAM_BOT_TOKEN"):
        raise Exception("Missing BIBA_TELEGRAM_BOT_TOKEN environment variable")
    if not os.environ.get("BIBA_TELEGRAM_CHANNEL"):
        raise Exception("Missing BIBA_TELEGRAM_CHANNEL environment variable")
    if not os.environ.get("BIBA_ESPN_LEAGUEID"):
        raise Exception("Missing BIBA_ESPN_LEAGUEID environment variable")
    if not os.environ.get("BIBA_ESPN_LEAGUE_YEAR"):
        raise Exception("Missing BIBA_ESPN_LEAGUE_YEAR environment variable")
    if not os.environ.get("BIBA_ESPN_S2"):
        raise Exception("Missing BIBA_ESPN_S2 environment variable")
    if not os.environ.get("BIBA_ESPN_SWID"):
        raise Exception("Missing BIBA_ESPN_SWID environment variable")

def get_bot_handler() -> BotHandler:
    check_environment_variables()
    
    cfg_bot_token = os.environ.get("BIBA_TELEGRAM_BOT_TOKEN")
    cfg_bot_channel = os.environ.get("BIBA_TELEGRAM_CHANNEL")
    
    cfg_espn_leagueid = os.environ.get("BIBA_ESPN_LEAGUEID")
    cfg_espn_leagueyear = int(os.environ.get("BIBA_ESPN_LEAGUE_YEAR"))
    cfg_espn_s2 = os.environ.get("BIBA_ESPN_S2")
    cfg_espn_swid = os.environ.get("BIBA_ESPN_SWID")
    league = League(league_id=cfg_espn_leagueid,
                    year=cfg_espn_leagueyear,
                    espn_s2=cfg_espn_s2,
                    swid=cfg_espn_swid)

    ## For testing purposes use the LogBot, it won't spam Telegram
    # from bibabot.LogBot import LogBot
    # bot = LogBot()
    bot = TelegramBot(cfg_bot_token, cfg_bot_channel)
    commands = [
        BibaCommand(),
        RecentActivityCommand(league, TIMER_DURATION_SECS),
        ]
    return BotHandler(bot, commands)

## Timer trigger
@app.function_name(name="transfer_update")
@app.timer_trigger(arg_name="timer",
                   schedule="0 0 * * * *", # TODO: How to translate TIMER_DURATION_SECS to cron syntax
                   run_on_startup=False)
def transfer_update(timer: func.TimerRequest) -> None:
    logging.info('[transfer_update] triggered via Timer!')
    try:
        bot_handler = get_bot_handler()
        bot_handler.handle_command("/activity")
    except Exception as ex:
        logging.exception("Cannot run Function without proper environment being configured, aborting...")
        return

# HTTP trigger
@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP function triggered!')
    data = req.get_json()
    logging.info(pformat(data))
    
    try:
        command = data['message']['text']
        bot_handler = get_bot_handler()
        bot_handler.handle_command(command)
    except Exception as ex:
        logging.exception("Cannot run Function without proper environment being configured, aborting...")
        return func.HttpResponse("Internal Server Error", status_code=500)

    return func.HttpResponse("OK", status_code=200)
