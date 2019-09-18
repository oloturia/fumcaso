#!/usr/bin/env python3
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import csv
import random

def replaceText(text):
	with open("subs.csv") as rtext:
		csvReader = csv.reader(rtext,delimiter=";")
		for row in csvReader:
			if text.find(row[0]) != -1:
				text = text.replace(row[0],row[random.randint(1,len(row)-1)])
				return text

def fetchText(indText):
	with open("rtext.csv") as rtext:
		csvReader = csv.reader(rtext,delimiter=';')
		for row in csvReader:
			if row[0]==indText:
				if len(row)>2:
					return row[1],row[2],row[random.randint(3,len(row)-1)].replace('@','\n')
				else:
					return 0
					
def fetch2Text(indText):
		with open("r2text.csv") as rtext:
			csvReader = csv.reader(rtext,delimiter=';')
			for row in csvReader:
				if row[0]==indText:
					if len(row)>2:
						rand1 = random.randint(5,len(row)-1)
						if rand1 %2 == 0:
							rand1 -=1
						rand2 = rand1+1
						return row[1],row[2],row[3],row[4],row[rand1].replace('@','\n'),row[rand2].replace('@','\n')
					else:
						return 0
					
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
		story[nvign]+=".png"
		nvign +=1
	return story
		
def addThing(indVign):
	with open("obj.csv") as obj:
		csvReader = csv.reader(obj)
		for row in csvReader:
			if row[0] == indVign:
				return row[random.randint(3,len(row)-1)],row[1],row[2]
		return 0

def writeStrip(story):
	strip = []
	for indVign in story:
		if indVign!="000":
			vign = Image.open(indVign).convert('RGBA')
			addtext = ImageDraw.Draw(vign)
			fnt = ImageFont.truetype("ubuntu.ttf",16)
			if indVign[0] == 'A':
				textVign = fetchText(indVign)
				if textVign !=0:
					text1 = textVign[2]
					if text1.find('$') != -1:
						text1 = replaceText(text1)
					addtext.multiline_text((int(textVign[0]),int(textVign[1])),text1,fill="#000000",font=fnt,align="center")
			else:
				textVign = fetch2Text(indVign)
				if textVign!=0:
					text1 = textVign[4]
					text2 = textVign[5]
					if text1.find('$') != -1:
						text1 = replaceText(text1)
					if text2.find('$') != -1:
						text2 = replaceText(text2)
					addtext.multiline_text((int(textVign[0]),int(textVign[1])),text1,fill="#000000",font=fnt,align="center")
					addtext.multiline_text((int(textVign[2]),int(textVign[3])),text2,fill="#000000",font=fnt,align="center")
			obj = addThing(indVign)
			if obj!=0:
				objImg = Image.open(obj[0])
				vign.paste(objImg,(int(obj[1]),int(obj[2])))
			strip.append(vign)
	image = Image.new('RGBA',(2400,500))
	xshift=0
	for vign in strip:
		image.paste(vign,(xshift,0))
		xshift += 600
	return image

def createStrip(name):
	try:
		story = fetchVign()
		finalStrip = writeStrip(story)
		finalStrip.save(name)
		return 0
	except Exception as err:
		return err

if __name__ == "__main__":
	story = fetchVign()
	finalStrip = writeStrip(story)
	finalStrip.show()
