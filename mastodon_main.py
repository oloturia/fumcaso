#!/usr/bin/env python3
from randstrip import createStrip
from mastodon import Mastodon
import os.path
		
if __name__ == "__main__":
	with open("createapp") as f:
		createapp = f.readlines()
	createapp = [x.strip() for x in createapp]
	app = createapp[0]
	api_base_url_cr = createapp[1]
	to_file_cr = createapp[2]
	email = createapp[3]
	pw = createapp[4]
	if os.path.exists(content[2]) == False:
		Mastodon.create_app(
			app,
			api_base_url = api_base_url_cr,
			to_file = to_file_cr
		)
	mastodon = Mastodon(
		client_id = to_file_cr,
		api_base_url = api_base_url_cr
	)
	mastodon.log_in(
		email,
		pw,
		to_file = to_file_cr
	)
	
	mastodon = Mastodon(
		access_token = to_file_cr
		api_base_url = api_base_url_cr
	)
	status = createStrip("mastodon.png")
	if status == 0:
		mastodon.media_post("mastodon.png","image/png")
	else:
		print("error creating image\n")
		print status
