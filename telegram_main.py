#!/usr/bin/python3
from telegram.ext import Updater, CommandHandler
from randstrip import createStrip,readConfig
import requests
import os

fileDir = os.path.dirname(os.path.abspath(__file__))
fileDir = fileDir +"/"

def newStrip(bot, update, args):
	config = readConfig(platform="telegram",profile=args)
	status = createStrip(config)
	if status == 0:
		try:
			bot.send_photo(chat_id=update.message.chat_id,photo=open(config["saveLocation"]+config["filename"],"rb"))
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
	updater = Updater(token)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler('strip',newStrip, pass_args=True))
	updater.start_polling()
	updater.idle()
