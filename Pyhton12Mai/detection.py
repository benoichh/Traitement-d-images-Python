from PIL import Image
import sys

from os import listdir

percent = 0.95
side = 30

#Fonction exécuter lorsque l'on lance le programme
def Start():
	files = listdir(sys.argv[1])

	for f in files:
		if f.endswith(".jpg") or f.endswith(".png") :
			img = Image.open(sys.argv[1]+"/"+f)
			image = reconize(img)
			image.save(sys.argv[2]+"/"+"detecte_"+ f)


#Fonction permettant de calculer la distance euclidienne entre 2 points
def eucl(x1,y1,x2,y2):
	return ((x1-x2)**2+(y1-y2)**2)**0.5


#Fonction permettant de reconnaître la censure en essaynt de trouver des pixels de même couleurs côte à côte
def reconize(img):

	pixR = img.load()
	thumb = img.copy()
	pix = thumb.load()

	list_X = []
	list_Y = []
	print("step 1")
	#Reconnaître des pixels similaires côte à côte
	for x in range(0,img.size[0]-side, side):

		if x%20==0: print((100*x)/(img.size[0]-side))
		for y in range(0,img.size[1]-side,side):

			if(pix[x,y] != (0,0,255)):

				cmpt = 0

				for xp in range(x,x+side):
					for yp in range(y,y+side):
						if(soustraction(pixR[xp,yp],pixR[x,y]) <= 3):
							cmpt += 1

				if(cmpt >= side*side*percent):
					for xp in range(x,x+side):
						for yp in range(y,y+side):
							list_X.append(xp)
							list_Y.append(yp)
							
	

	for i in range(len(list_X)):
		X = list_X[i]
		Y = list_Y[i]

		pix[X,Y] = 0,0,255							


	print("step 2")
    #Reconnaître des rectangle à 90% de bleu
	for x in range(0,img.size[0]-side,side):
		if x%20==0: print((100*x)/(img.size[0]-side))
		for y in range(0,img.size[1]-side,side):
			
			if(pix[x,y] == (0,0,255)):

				cmpt2 = 0

				for xp in range(x,x+side):
					for yp in range(y,y+side):
						if(pix[xp,yp]==(0,0,255)):
							cmpt2 += 1
			
				if(cmpt2 >= side*side*percent):
					for xp in range(x+1,x+side):
						for yp in range(y+1,y+side):
							pix[xp, yp] = 0,0,255


	thumb.show()
	return thumb
	pass


#Fonction permettant la soustraction entre 2 pixels
def soustraction(pix1, pix2):

	R1,G1,B1 = pix1
	R2,G2,B2 = pix2
	
	R = abs(R1-R2)
	G = abs(G1-G2)
	B = abs(B1-B2)
	
	#pix3 = R,G,B
	total = R+G+B
	
	#return pix3
	return total


Start()
