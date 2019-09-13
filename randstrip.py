#!/usr/bin/env python3
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import csv
import random

def fetchText(indText):
	with open("rtext.csv") as rtext:
		csvReader = csv.reader(rtext,delimiter=';')
		for row in csvReader:
			if row[0]==indText:
				return row[1],row[2],row[random.randint(3,len(row)-1)].replace('@','\n')
				
def fetch2Text(indText):
		with open("r2text.csv") as rtext:
			csvReader = csv.reader(rtext,delimiter=';')
			for row in csvReader:
				if row[0]==indText:
					rand1 = random.randint(5,len(row)-1)
					if rand1 %2 == 0:
						rand1 +=1
					rand2 = rand1+1
					return row[1],row[2],row[3],row[4],row[rand1].replace('@','\n'),row[rand2].replace('@','\n')
					
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
			if indVign[0] == 'A':
				textVign = fetchText(indVign)
				addtext.multiline_text((int(textVign[0]),int(textVign[1])),textVign[2],fill="#000000",font=fnt,align="center")
			else:
				textVign = fetch2Text(indVign)
				addtext.multiline_text((int(textVign[0]),int(textVign[1])),textVign[4],fill="#000000",font=fnt,align="center")
				addtext.multiline_text((int(textVign[2]),int(textVign[3])),textVign[5],fill="#000000",font=fnt,align="center")
			vign.show()

if __name__ == "__main__":
	#story = fetchVign()
	#writeStrip(story)
	writeStrip(["A00.png"])
