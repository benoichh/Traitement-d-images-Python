#python3 makeMosaique.py Images 30  ImagesCensuree

from PIL import Image
import sys
import random

from os import listdir


Files = listdir(sys.argv[1])

for f in Files:

	im = Image.open(sys.argv[1]+"/"+f)
	im.show()

	radius = int(sys.argv[2])
	black = False

	if(len(sys.argv) > 3 and sys.argv[3] == "black"):
		black = True

	thumb = im.copy()
	thumb.thumbnail((im.size[0]//radius, im.size[1]//radius))
	pix = thumb.load()
	thumb.show()

	for i in range(10):
		X = random.randrange(0, im.size[0]-radius, radius)
		Y = random.randrange(0, im.size[1]-radius, radius)
		W = random.randint(1,10)
		H = random.randint(1,10)

		for j in range(W):
			x = X+j*radius
			if x+radius >= im.size[0]:
				break

			for k in range(H):
				y = Y+k*radius
				if y+radius >= im.size[1]:
					break



				box = (x,y,x+radius, y+radius)
				if black:
					im.paste((0,0,0), box)
				else:
					im.paste(pix[x//radius,y//radius], box)

	im.show()
	im.save(sys.argv[3]+"/"+"censure_"+ f)

	#Comment trouver les coordonnées modifiées?
	listCoord = (X,Y)
	#Comment enlever le .png ?
	Fichier = open("Coordonnee/"+ f + ".txt", "a")

	for i in range(len(listCoord)):
		Fichier.write(listCoord[i])
