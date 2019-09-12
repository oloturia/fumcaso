#!/usr/bin/env python3
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import csv
import random

def fetchText(indText):
	with open("rtext.csv") as rtext:
		csvReader = csv.reader(rtext)
		for row in csvReader:
			if (row[0]==indText):
				return row[random.randint(1,len(row)-1)] 
				
def fetchVign():
	starts = []
	startdest = []
	nvign = 0
	currVign = "000"
	story = []
	with open("ram.csv") as ram:
		csvReader = csv.reader(ram)
		for row in csvReader:
			starts.append(row[0])
			startdest.append(row)
	while nvign <= 3:
		story.append(startdest[starts.index(currVign)][random.randint(1,len(startdest[starts.index(currVign)])-1)])
		currVign = story[nvign]
		if story[nvign] == "B00":
			story[nvign] += "."
			story[nvign] += str(random.randint(0,2))
		nvign +=1
	return story
		
def writeStrip(story):
	for indVign in story:
		if indVign!="000":
			vign = Image.open(indVign)
			addtext = ImageDraw.Draw(vign)
			fnt = ImageFont.truetype("ubuntu.ttf",16)
			textVign = fetchText(indVign)
			print(textVign)
			addtext.text((268,77),textVign,fill="#000000",font=fnt)
			vign.show()

if __name__ == "__main__":
	#story = fetchVign()
	#writeStrip(story)
	writeStrip(["A00.png"])
