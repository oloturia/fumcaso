#!/usr/bin/env python3
from telegram.ext import Updater, CommandHandler
from randstrip import createStrip
import requests
import os

fileDir = os.path.dirname(os.path.abspath(__file__))
fileDir = fileDir +"/"

def newStrip(bot, update):
	status = createStrip("telegram.png")
	if status == 0:
		try:
			bot.send_photo(chat_id=update.message.chat_id,photo=open(fileDir+"telegram.png","rb"))
		except Exception as err:
			print(err)
	else:
		print("Creation of image failed\n")
		print(status)
	
if __name__ == "__main__":
	with open(fileDir+"telegram_token") as token_file:
		content = token_file.readlines()
	token = content[0].strip()
	updater = Updater(token)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler('strip',newStrip))
	updater.start_polling()
	updater.idle()