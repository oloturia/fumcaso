#!/usr/bin/env python3
import tweepy
from randstrip import createStrip
import os

fileDir = os.path.dirname(os.path.abspath(__file__))
fileDir = fileDir +"/"

if __name__ == "__main__":
	status = createStrip("twitter.png")
	if status == 0:
		with open(fileDir+"twitter_token") as f:
			tokens = f.readlines()
		tokens = [x.strip() for x in tokens]
		auth = tweepy.OAuthHandler(tokens[0],tokens[1])
		auth.set_access_token(tokens[2],tokens[3])
		api = tweepy.API(auth)
		try:
			api.verify_credentials()
			api.update_with_media(fileDir+"twitter.png","Generatore automatico di strip. Striscia di oggi.")
		except:
			print("Auth error")
	else:
		print("Error creating image\n")
		print(status)
