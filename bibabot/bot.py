
import telebot

def get_bot(bot_token):
    return telebot.TeleBot(bot_token)

def handle_biba(bot_token, bot_channel):
    bot = get_bot(bot_token)
    bot.send_message(bot_channel, f'Hello this is Bibabot!')
    