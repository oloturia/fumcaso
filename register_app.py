#!/usr/bin/env python3
from mastodon import Mastodon

'''
you need to register the app only once
'''


Mastodon.create_app(
	"oloturia_listener",
	api_base_url = "https://botsin.space",
	to_file = "secret"
)

print("App registered!")
