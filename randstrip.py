#!/usr/bin/python3
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import csv
import random
import os
import json

fileDir = os.path.dirname(os.path.abspath(__file__))


def replaceText(text,config):
	"""This function replace $WILDCARD with a word found in subs.csv
	subs.csv definition is 1st colum $WILDCARD, subsequent columns, possible values (chosen at random), delimiter is ;"""
	with open(config["csvLocation"]+"/"+config["csvSubs"]) as subs: 
		csvReader = csv.reader(subs,delimiter=";") 
		for row in csvReader:
			if text.find(row[0]) != -1:
				text = text.replace(row[0],row[random.randint(1,len(row)-1)],1)
				return text

def fetchText(indText,config):
	"""This function fetch the text for the image with two characters
	rtext.csv definition is: 1st column the name of the file (i.e. B001.png), 2nd number of actors (at the moment
	they are limited to two; then a couple of columns or each actor with x and y coord of the strings; after the coords the outcomes, 
	one column for each actor
	Delimiter is ; and line feeds @, if there aren't any options, it returns 0 (no text)
	It returns two arrays, coords is a tuple (x,y) and result is the outcome"""
	with open(config["csvLocation"]+"/"+config["csvSpeech"]) as rtext:
		csvReader = csv.reader(rtext,delimiter=';')
		for row in csvReader:
			if row[0]==indText:
				noActors = int(row[1])
				if noActors == 0:
					return 0
				else:
					firstElement = 2+(noActors*2)
					lastElement = len(row)-(noActors-1)
					randQuote = random.randrange(firstElement,lastElement,noActors)
					coords = []
					result = []
					for x in range(0,noActors):
						coords.append((row[2+x*2],row[3+x*2]))
						result.append(row[randQuote+x])
					return coords,result

				
def fetchVign(config):
	"""This functions fetch an image, randomly, chosen from a markov tree defined in ram.csv
	ram.csv definition is: 1st column the name of the image (without extension), subsequent columns, possible outcomes chosen randomly
	It returns an array with the file names"""
	starts = []
	startdest = []
	nvign = 0
	currVign = "000"
	story = []
	with open(config["csvLocation"]+"/"+config["csvTree"]) as ram:
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
		
def addThing(indVign,config):
	"""This function adds a small image (object) to a larger image
	obj.csv definition is: name of the image (i.e. A001.png), x-coord, y-coord, subsequent columns possible outcomes
	It returns a tuple (object file name, x, y)"""
	with open(config["csvLocation"]+"/"+config["csvObj"]) as obj:
		csvReader = csv.reader(obj)
		for row in csvReader:
			if row[0] == indVign:
				return row[random.randint(3,len(row)-1)],row[1],row[2]
		return 0

def writeStrip(story,fontSize,config):
	"""This function creates the strip returning an image object that could be saved or viewed. It takes an array with filenames as parameter
	The first image is always 000, then appends to strip the files, then decorates it fetching text and adding objects. If the object is an R, then
	repeats the last object."""
	strip = []
	for indVign in story:
		try:
			vign = Image.open(config["imagesLocation"]+"/"+indVign).convert('RGBA')
			addtext = ImageDraw.Draw(vign)
			fnt = ImageFont.truetype(config["font"],fontSize)
			textVign = fetchText(indVign,config)
			
			if textVign!=0:
				try:
					for x in range(len(textVign[0])):
						text_vign = textVign[1][x]
						try:
							while text_vign.find('$') != -1:
								text_vign = replaceText(text_vign,config)
						except AttributeError:
							print("Problem parsing:")
							print(textVign)
							quit()
						text_vign = text_vign.replace('@','\n')
						addtext.multiline_text((int(textVign[0][x][0]),int(textVign[0][x][1])),text_vign,fill="#000000",font=fnt,align="center")
				except TypeError:
					print("Problem finding text for:")
					print(indVign)
					quit()
					
			obj = addThing(indVign,config)
			if obj!=0:
				if obj[0] == 'R':
					objImg = Image.open(config["imagesLocation"]+"/"+prevObj[0])
				else:
					prevObj = obj
					objImg = Image.open(config["imagesLocation"]+"/"+obj[0])
				vign.paste(objImg,(int(obj[1]),int(obj[2])))
			strip.append(vign)
		except FileNotFoundError:
			pass
	image = Image.new('RGBA',(config["xSize"],config["ySize"]))
	xshift=0
	for vign in strip:
		image.paste(vign,(xshift,0))
		xshift += config["panelLength"]
	return image

def createStrip(config,specialPlatform="",fontSize=22):
	"""Create strip and save it
	createStrip(str path/filename)"""

	try:
		story = fetchVign(config)
		finalStrip = writeStrip(story,fontSize,config)
		if specialPlatform == "android":
			return finalStrip
		else:
			finalStrip.save(config["saveLocation"]+config["filename"])
			return 0
	except Exception as err:
		return err

def readConfig(profile=False,platform=False):
	"""Read configuration file"""
	try:
		with open(fileDir+"/config.json") as f:
			config = json.load(f)
	except IOError:
		print("config.json not found")
		return False
	if not(profile):
		profile = config["defaultProfile"]
	else:
		profile = profile[0]
	try:
		checkProfile = config[profile]
	except KeyError:
		print("Profile "+profile+" not found")
		quit()
	saveLocation = checkLocal(config[profile]["saveLocation"])
	imagesLocation = checkLocal(config[profile]["imagesLocation"])
	csvLocation = checkLocal(config[profile]["csvLocation"])
	csvTree = config[profile]["csvTree"]
	csvSpeech = config[profile]["csvSpeech"]
	csvSubs = config[profile]["csvSubs"]
	csvObj = config[profile]["csvObj"]
	font = checkLocal(config[profile]["font"])
	xSize = config[profile]["xSize"]
	ySize = config[profile]["ySize"]
	panelLength = config[profile]["panelLength"]
	if platform:
		token = checkLocal(config[profile][platform]["token"])
		filename = checkLocal(config[profile][platform]["filename"])
		try:
			text = config[profile][platform]["text"]
		except KeyError:
			postText = False
		
		return {"saveLocation":saveLocation,"imagesLocation":imagesLocation,"csvLocation":csvLocation,"font":font,"token":token,"filename":filename,"xSize":xSize,"ySize":ySize,"panelLength":panelLength,"csvTree":csvTree,"csvSpeech":csvSpeech,"csvSubs":csvSubs,"csvObj":csvObj,"text":text}
	filename = config[profile]["filename"]
	return {"saveLocation":saveLocation,"imagesLocation":imagesLocation,"csvLocation":csvLocation,"font":font,"filename":filename,"xSize":xSize,"ySize":ySize,"panelLength":panelLength,"csvTree":csvTree,"csvSpeech":csvSpeech,"csvSubs":csvSubs,"csvObj":csvObj}
		
def checkLocal(directory):
	"""Checks if it's a relative or absolute path"""
	if directory[0] == ".":
		return fileDir + directory[1:]
	else:
		return directory
	

if __name__ == "__main__":
	import argparse


	parser = argparse.ArgumentParser()
	parser.add_argument('-s','--story',metavar='story',default='',nargs=4,help='name of the images')
	parser.add_argument('-m','--multiple',metavar='multiple',default=[1],nargs=1,type=int,help='multiple output (int >0)')
	parser.add_argument('-x','--xsize',metavar='xsize',default=0,type=int,nargs=1,help='resize image x')
	parser.add_argument('-p','--profile',metavar='profile',default="",type=str,nargs=1,help='profile')
	parser.add_argument('-o','--output',metavar='output',const=True,default=False,nargs="?",help='output file, if name not specified, default path will be used')
	args = parser.parse_args()
	
	if args.multiple[0] <= 0:			#Wrong multiple choice
		quit()
	config = readConfig(profile=args.profile)
	
	if args.output == True:				#Output on but no filename specified
		fileName = config["saveLocation"]+config["filename"]
	elif type(args.output) == str:		#Output specified
			fileName = args.output

	for ist in range(0,args.multiple[0]):
		if (args.story == ''):			#No story specified
			story = fetchVign(config)
		else:
			story = []					#Story specified
			for x in args.story:
				story.append(x)
		finalStrip = writeStrip(story,22,config)
		
		if args.xsize != 0:				#Resize specified
			finalStrip = finalStrip.resize((args.xsize[0],int(args.xsize[0]/2400*500)))
		
		if args.multiple[0] == 1:		#No multiple selected
			if args.output == False:
				finalStrip.show()
			else:
				finalStrip.save(fileName)
		else:							#Multiple selected
			if args.output == False:
				print(story)
			else:
				finalStrip.save(str(ist)+fileName+".png")
			
			
			
