#!/usr/bin/python3

from randstrip import createStrip,readConfig
from mastodon import Mastodon
import os
import sys

fileDir = os.path.dirname(os.path.abspath(__file__))
fileDir = fileDir + "/"
API_URL = "https://botsin.space"

if __name__ == "__main__":
	config = readConfig


