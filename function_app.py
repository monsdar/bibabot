import azure.functions as func

import os
import logging
from pprint import pformat
import telebot

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

def get_bot():
    cfg_bot_token = os.environ.get("BIBA_TELEGRAM_BOT_TOKEN")
    return telebot.TeleBot(cfg_bot_token)

def handle_biba():
    bot = get_bot()
    cfg_bot_channel = os.environ.get("BIBA_TELEGRAM_CHANNEL")
    bot.send_message(cfg_bot_channel, f'Hello this is Bibabot!')

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

    cfg_espn_leagueid = os.environ.get("BIBA_ESPN_LEAGUEID")
    cfg_espn_leagueyear = os.environ.get("BIBA_ESPN_LEAGUE_YEAR")
    cfg_espn_s2 = os.environ.get("BIBA_ESPN_S2")
    cfg_espn_swid = os.environ.get("BIBA_ESPN_SWID")

    text = data['message']['text']
    if text.startswith("/biba"):
        handle_biba()

    return func.HttpResponse("OK", status_code=200)


###
# Telegram Data in Request:
###
sample_req = {
    'message': {'chat': {'all_members_are_administrators': True,
                         'id': -12345678,
                         'title': 'Channel_Name',
                         'type': 'group'},
                'date': 1728156449,
                'entities': [{'length': 5, 'offset': 0, 'type': 'bot_command'}],
                'from': {'first_name': 'John',
                         'id': 123456789,
                         'is_bot': False,
                         'language_code': 'en',
                         'last_name': 'doe',
                         'username': 'pu$$ykiller69'},
                'message_id': 1678,
                'text': '/test'},
    'update_id': 123456789}
