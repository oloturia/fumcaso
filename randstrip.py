#!/usr/bin/env python3
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import csv
import random
import os

fileDir = os.path.dirname(os.path.abspath(__file__))
fileDir = fileDir +"/"


def replaceText(text):
	"""This function replace $WILDCARD with a word found in subs.csv
	subs.csv definition is 1st colum $WILDCARD, subsequent columns, possible values (chosen at random), delimiter is ;"""
	with open(fileDir+"subs.csv") as rtext: 
		csvReader = csv.reader(rtext,delimiter=";") 
		for row in csvReader:
			if text.find(row[0]) != -1:
				text = text.replace(row[0],row[random.randint(1,len(row)-1)],1)
				text = text.replace('@','\n')
				return text

#def fetchText(indText):	
#	"""This function fetch the text for the image with just only one character
#	rtext.csv definition is: 1st column the name of the file (i.e. A001.png), 2nd x-coord, 3rd y-coord, 4th and subsequent, the possible outcomes
#	Delimiter is ; and line feeds @, if there aren't any options, it returns 0 (no text)
#	It returns a tuple (x,y,text)"""
#	with open(fileDir+"rtext.csv") as rtext:
#		csvReader = csv.reader(rtext,delimiter=';')
#		for row in csvReader:
#			if row[0]==indText:
#				if len(row)>2:
#					return row[1],row[2],row[random.randint(3,len(row)-1)].replace('@','\n')
#				else:
#					return 0

def fetchText(indText):
	"""This function fetch the text for the image with two characters
	rtext.csv definition is: 1st column the name of the file (i.e. B001.png), 2nd x-coord, 3rd y-coord of the first string
	4th x-coord, 5th y-coord of the second string, 6th and subsequent are the outcomes, alternated as the odd one is an
	answer to the even one
	Delimiter is ; and line feeds @, if there aren't any options, it returns 0 (no text)
	It returns a tuple(x1,y1,x2,y2,text1,text2)"""
	with open(fileDir+"rtext.csv") as rtext:
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
	"""This functions fetch an image, randomly, chosen from a markov tree defined in ram.csv
	ram.csv definition is: 1st column the name of the image (without extension), subsequent columns, possible outcomes chosen randomly
	It returns an array with the file names"""
	starts = []
	startdest = []
	nvign = 0
	currVign = "000"
	story = []
	with open(fileDir+"ram.csv") as ram:
		csvReader = csv.reader(ram)
		for row in csvReader:
			starts.append(row[0])
			startdest.append(row)
	while nvign <100:
		story.append(startdest[starts.index(currVign)][random.randint(1,len(startdest[starts.index(currVign)])-1)])
		currVign = story[nvign]
		if currVign == "END":
			return story
		story[nvign]+=".png"
		nvign +=1
	print("tree with no END")
	quit()
		
def addThing(indVign):
	"""This function adds a small image (object) to a larger image
	obj.csv definition is: name of the image (i.e. A001.png), x-coord, y-coord, subsequent columns possible outcomes
	It returns a tuple (object file name, x, y)"""
	with open(fileDir+"obj.csv") as obj:
		csvReader = csv.reader(obj)
		for row in csvReader:
			if row[0] == indVign:
				return row[random.randint(3,len(row)-1)],row[1],row[2]
		return 0

def writeStrip(story,fontSize):
	"""This function creates the strip returning an image object that could be saved or viewed. It takes an array with filenames as parameter
	The first image is always 000, then appends to strip the files, then decorates it fetching text and adding objects. If the object is an R, then
	repeats the last object."""
	strip = []
	for indVign in story:
		#if indVign!="000":
		try:
			vign = Image.open(fileDir+indVign).convert('RGBA')
			addtext = ImageDraw.Draw(vign)
			fnt = ImageFont.truetype(fileDir+"ubuntu.ttf",fontSize)
			textVign = fetchText(indVign)
			if textVign!=0:
				text1 = textVign[4]
				text2 = textVign[5]
				while text1.find('$') != -1:
					text1 = replaceText(text1)
				while text2.find('$') != -1:
					text2 = replaceText(text2)
				addtext.multiline_text((int(textVign[0]),int(textVign[1])),text1,fill="#000000",font=fnt,align="center")
				addtext.multiline_text((int(textVign[2]),int(textVign[3])),text2,fill="#000000",font=fnt,align="center")
			
			obj = addThing(indVign)
			if obj!=0:
				if obj[0] == 'R':
					objImg = Image.open(fileDir+prevObj[0])
				else:
					prevObj = obj
					objImg = Image.open(fileDir+obj[0])
				vign.paste(objImg,(int(obj[1]),int(obj[2])))
			strip.append(vign)
		except FileNotFoundError:
			pass
	image = Image.new('RGBA',(2400,500))
	xshift=0
	for vign in strip:
		image.paste(vign,(xshift,0))
		xshift += 600
	return image

def createStrip(name,fontSize=22):
	"""Create strip and save it
	createStrip(str path/filename)"""
	try:
		story = fetchVign()
		finalStrip = writeStrip(story,fontSize)
		if name == "android":
			return finalStrip
		else:
			finalStrip.save(fileDir+name)
			return 0
	except Exception as err:
		return err

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-s','--story',metavar='story',default='',nargs=4,help='name of the images')
	args = parser.parse_args()
	if (args.story == ''):
		story = fetchVign()
	else:
		story = []
		for x in args.story:
			story.append(x)
	print(story)
	finalStrip = writeStrip(story,22)
	finalStrip.show()
