#!/usr/bin/python3
import tweepy
from randstrip import createStrip,readConfig
import os
import sys

fileDir = os.path.dirname(os.path.abspath(__file__))
fileDir = fileDir +"/"

if __name__ == "__main__":
	if len(sys.argv) == 2:
		altProfile = [sys.argv[1]]
	else:
		altProfile = False
	config = readConfig(platform="twitter",profile=altProfile)
	status = createStrip(config)
	if status == 0:
		with open(config["token"]) as f:
			tokens = f.readlines()
		tokens = [x.strip() for x in tokens]
		auth = tweepy.OAuthHandler(tokens[0],tokens[1])
		auth.set_access_token(tokens[2],tokens[3])
		api = tweepy.API(auth)
		published = False
		for i in range(0,100):
			try:
				api.verify_credentials()
				api.update_with_media(config["saveLocation"]+config["filename"],config["text"])
				published = True
				os.remove(config["saveLocation"]+config["filename"])
			except:
				continue
			break
		
		if not(published):
			print("Auth error")
	else:
		print("Error creating image\n")
		print(status)
