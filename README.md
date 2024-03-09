# fumcaso
Random Comic Generator/Bot

randstrip.py - Create a random strip and show it with ImageMagick.

mastodon_main.py - Publish a new strip on Mastodon.

twitter_main.py - Publish a new strip on Twitter.

telegram_main.py - Launches the Telegram bot.


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

Configuration is JSON file. This is an example:

    {
        defaultProfile: 		name of the profile used if not specified
        "profile name" :{		name of the profile
		saveLocation: 		location for temporary files
		filename:		default filename used by function createStrip, if not specified (not used in any of the scripts, at the moment)
		imagesLocation:		folder where the different panels are stored
		csvLocation:		folder where the csv are stored
		csvTree:		name of file containing panel chains
		csvSpeech:		name of file containing speech
		csvSubs:		name of file containing substitutions in text
		csvObj:			name of file containing information about objects location
		csvAltText:		name of file containing alternate text
		xSize:			width of the final image
		ySize:			height of the final image
		panelLength:		length of a single panel (roughly panelLength * number-of-panels / panelsPerRow should be = xSize)
  		panelHeight:		height of a single panel (roughly panelHeight * number-of-panels / panelsPerRow should be = ySize)
    		panelsPerRow:		number of panels per single row
		font:			font used
  		fontSize:		size of font
		"application":{ 	special instruction for applications, like "twitter", "mastodon", "telegram"
			"token"		token location
			"filename"	filename used for the temporary image
			"text"		text for the post on Twitter and Mastodon (optional)
		}
        }
    }

There are four different csv files:

csvTree		Contains the chain (markov-like) about how the different panels are combined. The first column is the previous panel, other columns are the different possible outcomes.
		It always starts with 000, if a file is not found it does nothing, it ends with END.
		The script adds ".png" to the entries.
		
		origin,	destination, destination, destination...

csvSpeech	Contains the random text table. In the first column there is the name of the panel, then the number of actors, then the location (x and y) on the panel
		for text of each actor, then the random text. If there are more than one actors, the text is "1st location,2nd location" so if we have two
		characters speaking, that would be "question,answer". For silent panels, just put 0 in the 2nd column. For a line break put @. Different
	 	words can be randomly chosen with a substitution tag, tags are marked with a dollar sign, (like $TAG).
		
		name.png,0 				(silent panel name.png)
		name.png,1,100,200,Hello,Hi		(single character that says "Hello" or "Hi" placing text on x100 y200)
		name.png,2,100,200,300,200,Hello,Hi	(two characters, the first says "Hello" the second answers "Hi", the first has text on x100 y200, the second on x300 y200)
		name.png,1,100,200,$GREETING		(single character that says a random greeting defined in subs.csv)

csvSubs	every $ tag is in the first column of this file, the tag is substituted with a random word in the following columns, it's possible to insert
		tags in the substitution text. This csv uses semicolons.
		
		$GREETING;Hi;Hello;Hallo		($GREETING is substituted with "Hi", "Hello" or "Hallo")
		$COLOUR;red;green;$GREETING		($COLOUR is substituted with "red", "green" or a random greeting)

csvObj		Contains the location of random objects that can be placed on a panel. On the first column there is the name of the panel (like A00.png), then the x
		and y placement on the panel, then different image files of the objects to choose from. If a "R" is placed instead of the list,
		the last object used is repeated
		
		panel.png,100,200,obj00.png,obj01.png	(on panel.png a random object chosen among obj00.png and obj01.png is placed at x100 y200)
		panel2.png,100,200,R			(on panel2.png the object used in the previous panel  is placed at x100 y200)
