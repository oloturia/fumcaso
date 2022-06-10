#!/usr/bin/python3
from randstrip import createStrip,readConfig
from mastodon import Mastodon
import os
import sys

fileDir = os.path.dirname(os.path.abspath(__file__))
fileDir = fileDir +"/"
API_URL = "https://botsin.space"
	
def publishStrip(altProfile=False,user=False):
	config = readConfig(platform="mastodon",profile=altProfile)
	with open(config["token"]) as f:
		createapp = f.readlines()
	createapp = [x.strip() for x in createapp]
	TOKEN = createapp[0]
	mastodon = Mastodon(access_token = TOKEN,api_base_url = API_URL)
	status = createStrip(config)
	if status == 0:
		published = False
		for i in range(1,100):
			try:
				new_strip = mastodon.media_post(config["saveLocation"]+config["filename"],"image/png")
				if not(user):
					mastodon.status_post(config["text"],media_ids=new_strip)
				else:
					mastodon.status_post(user+" "+config["text"],media_ids=new_strip,visibility="direct")
				os.remove(config["saveLocation"]+config["filename"])
				published = True
			except:
				continue
			break
		if not(published):
			print("Auth error")
	else:
		print("error creating image\n")
		print(status)

if __name__ == "__main__":
	if len(sys.argv) == 2:
		publishStrip([sys.argv[1]])
	else:
		publishStrip()
