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
  $ sudo apt-get install libssl-dev

- python-telegram-bot 
  $ pip3 install python-telegram-bot

Configuration file is a JSON with this tree:
{
	defaultProfile: 		the name of the profile used if not specified

	"profile name" :{		the name of the profile
		saveLocation: 		the location where the file is saved
		filename:		the default filename used by function createStrip, if not specified (not used in any of the scripts, at the moment)
		imagesLocation:		the folder where the different panels are stored
		csvLocation:		the folder where the csv are stored
		font:			the font used
		"application":{ 	special instruction for applications, like "twitter", "mastodon", "telegram"
			"token"		token location
			"filename"	the filename used for the temporary image
		}
	}
}

There are four different csv with instruction on how to compose a new strip.

ram.csv		this has the chain (markov-like) of the different panels, the first column is the previous panel, other columns are the possible outcomes;
		it starts always with 000, if the file is not found it just prints nothing (it can be useful), it ends with END
		when the story is completed, the script adds ".png" to the entries
		
		origin,	destination, destination, destination...

rtext.csv	the random text table, in the first column there is the name of the panel, then the number of actors, then the location, x and y, for the
		text of each actor, then the random text; if there are more than one actors, the text is "1st location,2nd location" so if we have two
		characters speaking, that would be "question,answer";for silent panels, just put 0 in the 2nd column;for a line break put @; different
	 	words can be randomly chosen with a substitution tag, tags are marked with a dollar sign, (like $TAG)
		
		name.png,0 				(silent panel name.png)
		name.png,1,100,200,Hello,Hi		(single character that says "Hello" or "Hi" placing text on x100 y200)
		name.png,2,100,200,300,200,Hello,Hi	(two characters, the first says "Hello" the second answers "Hi", the first has text on x100 y200, the second on x300 y200)
		name.png,1,100,200,$GREETING		(single character that says a random greeting defined in subs.csv)

subs.csv	every $ tag is in the first column of this file, the tag is substituted with a random word in the following columns, it's possible to insert
		tags in the substitution text; this csv uses semicolons
		
		$GREETING;Hi;Hello;Hallo		($GREETING is substituted with "Hi", "Hello" or "Hallo")
		$COLOUR;red;green;$GREETING		($COLOUR is substituted with "red", "green" or a random greeting)

obj.csv		this csv has the location of random objects that can be placed on the panel; on the first column there is the name of the panel, then the x
		and y of the location on the panel, the the possible image files of the objects; if a "R" is placed instead of the list of possible files,
		the last object used is repeated
		
		panel.png,100,200,obj00.png,obj01.png	(on panel.png a random object chosen among obj00.png and obj01.png is placed at x100 y200)
		panel2.png,100,200,R			(on panel2.png the object used in the previous panel  is placed at x100 y200)
