#!/usr/bin/python3

from randstrip import createStrip
from mastodon import Mastodon, StreamListener
from mastodon_main import publishStrip
import json
import os
import sys

fileDir = os.path.dirname(os.path.abspath(__file__))
fileDir = fileDir + "/"
API_URL = "https://botsin.space"

class stripListener(StreamListener):
	def on_notification(self, notification):
		try:
			account = "@"+notification["account"]["acct"]
			content = notification["status"]["content"]
			if content.find("help") != -1:
				mastodon.status_post("Hello "+account+" just send me a message with 'new strip' and the desired profile. Try with 'oloturia' (Italian), 'oloeng' (broken English) or 'olofra' (French). If not specified, Italian will be selected as default.",visibility="direct")
			elif content.find("new strip") != -1:
				if content.find("oloeng") != -1:
					profile = "oloeng"
				elif content.find("olofra") != -1:
					profile = "olofra"
				else:
					profile = "oloturia"
				publishStrip([profile],account)
		except KeyError:
			return
			

if __name__ == "__main__":
	with open(fileDir+"/config.json") as f:
		config = json.load(f)
	with open(fileDir+config["mastodonListenerToken"]) as f:
		createapp = f.readlines()
	createapp = [x.strip() for x in createapp]
	TOKEN = createapp[0]
	mastodon = Mastodon(access_token = TOKEN,api_base_url = API_URL)
	listener = stripListener()
	mastodon.stream_user(listener)
