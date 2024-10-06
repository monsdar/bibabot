import azure.functions as func

import os
import logging
from pprint import pformat

from bibabot.BotHandler import BotHandler
from bibabot.TelegramBot import TelegramBot

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

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

## Timer trigger
#@app.function_name(name="transfer_update")
#@app.timer_trigger(arg_name="timer",
#                   schedule="0 */5 * * * *",
#                   run_on_startup=False)
#def transfer_update(timer: func.TimerRequest) -> None:
#    logging.info('[transfer_update] triggered via Timer!')
#    handle_biba()

# HTTP trigger
@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP function triggered!')
    data = req.get_json()
    logging.info(pformat(data))
    
    try:
        check_environment_variables()
    except Exception as ex:
        logging.exception("Cannot run Function without proper environment being configured, aborting...")
        return 
    
    cfg_bot_token = os.environ.get("BIBA_TELEGRAM_BOT_TOKEN")
    cfg_bot_channel = os.environ.get("BIBA_TELEGRAM_CHANNEL")
    cfg_espn_leagueid = os.environ.get("BIBA_ESPN_LEAGUEID")
    cfg_espn_leagueyear = os.environ.get("BIBA_ESPN_LEAGUE_YEAR")
    cfg_espn_s2 = os.environ.get("BIBA_ESPN_S2")
    cfg_espn_swid = os.environ.get("BIBA_ESPN_SWID")

    telegram_bot = TelegramBot(cfg_bot_token, cfg_bot_channel)
    bot_handler = BotHandler(telegram_bot)
    ## For testing purposes use the LogBot, it won't spam Telegram
    # from bibabot.LogBot import LogBot
    # log_bot = LogBot()
    # bot_handler = BotHandler(log_bot)

    text = data['message']['text']
    if text.startswith("/biba"):
        bot_handler.handle_biba()

    return func.HttpResponse("OK", status_code=200)
