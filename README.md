# fumcaso
Random Comic Generator/Bot

randstrip.py [NAME] - create a random strip, writes [NAME] in png format, if name is not specified the image is shown with ImageMagick.

mastodon_main.py - Publish a new strip on Mastodon. The token must be in a file called "mastodon_token".

twitter_main.py - Publish a new strip on Twitter. The token must be in a file called "twitter_token".

telegram_main.py - Launches the Telegram bot. The token must be in a file called "telegram_token".


Libraries needed: 

twitter_main.py: 
- tweepy
  $ pip3 install tweepy

mastodon_main.py:
- Mastodon.py
  $ pip3 install Mastodon.py
  
telegram_main.py:
- libssl
  # apt-get install libssl-dev

- python-telegram-bot 
  $ pip3 install python-telegram-bot
  
