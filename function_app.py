import azure.functions as func

import os
import logging
from pprint import pformat

from bibabot import bot

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

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
    logging.info('HTTP trigger function processed a request.')
    data = req.get_json()
    logging.info(pformat(data))

    cfg_bot_token = os.environ.get("BIBA_TELEGRAM_BOT_TOKEN")
    cfg_bot_channel = os.environ.get("BIBA_TELEGRAM_CHANNEL")
    cfg_espn_leagueid = os.environ.get("BIBA_ESPN_LEAGUEID")
    cfg_espn_leagueyear = os.environ.get("BIBA_ESPN_LEAGUE_YEAR")
    cfg_espn_s2 = os.environ.get("BIBA_ESPN_S2")
    cfg_espn_swid = os.environ.get("BIBA_ESPN_SWID")

    text = data['message']['text']
    if text.startswith("/biba"):
        bot.handle_biba(cfg_bot_token, cfg_bot_channel)

    return func.HttpResponse("OK", status_code=200)
