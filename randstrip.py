from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import csv
import random

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
		
def writeStrip():
	vign = Image.open("A00.png")
	addtext = ImageDraw.Draw(vign)
	fnt = ImageFont.truetype("ubuntu.ttf",16)
	addtext.text((268,77),"egadrg",fill="#000000",font=fnt)
	return vign

if __name__ == "__main__":
	fetchVign()
