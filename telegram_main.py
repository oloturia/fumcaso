#!/usr/bin/python3
from telegram.ext import Updater, CommandHandler
from randstrip import createStrip,readConfig
import requests
import os

fileDir = os.path.dirname(os.path.abspath(__file__))
fileDir = fileDir +"/"

def newStrip(update, context):
    config = readConfig(platform="telegram",profile=context.args)
    status = createStrip(config)
    if status == 0:
        try:
            strip_file=open(config["saveLocation"]+config["filename"],"rb")
            context.bot.send_photo(chat_id=update.message.chat_id,photo=strip_file)
            strip_file.close()
            os.remove(config["saveLocation"]+config["filename"])
        except Exception as err:
            print(err)
    else:
        print("Creation of image failed\n")
        print(status)
    
if __name__ == "__main__":
    config = readConfig(platform="telegram")
    with open(config["token"]) as token_file:
        content = token_file.readlines()
    token = content[0].strip()
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('strip',newStrip, pass_args=True))
    updater.start_polling()
    updater.idle()
