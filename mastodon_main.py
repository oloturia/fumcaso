#!/usr/bin/env python3
from randstrip import createStrip
from mastodon import Mastodon
import os.path

API_URL = "https://botsin.space"
	
if __name__ == "__main__":
	with open("createapp") as f:
		createapp = f.readlines()
	createapp = [x.strip() for x in createapp]
	TOKEN = createapp[0]
	mastodon = Mastodon(access_token = TOKEN,api_base_url = API_URL)
	status = createStrip("mastodon.png")
	if status == 0:
		new_strip = mastodon.media_post("mastodon.png","image/png")
		mastodon.status_post("Nuova striscia",media_ids=new_strip)
	else:
		print("error creating image\n")
		print(status)
