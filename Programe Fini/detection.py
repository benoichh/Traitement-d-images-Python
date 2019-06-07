#python3 detection.py ImagesCensuree ImagesDetectee


from PIL import Image
import sys
import random
from os import listdir

import pandas as pd
import matplotlib.pyplot as plt


percent = 0.90

#faire un histo
def calculeSide(img,f):

	cop = img.copy()
	pix = cop.load()
	listeHisto = [0]*img.size[0]

	for x in range(img.size[0]):
		for y in range(img.size[1]):
			i = 0
			while(soustraction(pix[x,y],pix[x+i,y]) <= 2):
				i += 1
				if x+i >= img.size[0]:
					break
			
			listeHisto[i]+=1
	
	while listeHisto[-5:] == [0,0,0,0,0]:
		listeHisto = listeHisto[:-1]
	X = list(range(0,len(listeHisto)))
	dlisteHisto = [0]+[a-b for a,b in zip(listeHisto[1:],listeHisto[:-1])]
	ddlisteHisto = [0]+[a-b for a,b in zip(dlisteHisto[2:],dlisteHisto[:-2])]+[0]
	plt.plot(X[5:],listeHisto[5:],color = "black", lw = 2, alpha=1)
	plt.plot(X[5:],dlisteHisto[5:],color = "red", lw = 2, alpha=1)
	plt.plot(X[5:],ddlisteHisto[5:],color = "blue", lw = 2, alpha=1)
	
	plt.title("Nombres de pixel similaire côte à côte en fonction du pixels" + f)
	plt.xlabel("n° de Pixels")
	plt.ylabel("Nombres de pixel similaire côte à côte")
	#plt.show()
	plt.close()

	last = None
	Max = 0
	for n in range(3,len(listeHisto)-1):
		if(dlisteHisto[n] < 0 and dlisteHisto[n-1] > dlisteHisto[n] and dlisteHisto[n+1] > dlisteHisto[n]):
			if(Max < dlisteHisto[n-1]+dlisteHisto[n+1]-2*dlisteHisto[n]):
				Max = dlisteHisto[n-1]+dlisteHisto[n+1]-2*dlisteHisto[n]
				last = n-1
	print("radius : ", last)
	return last



#Fonction exécuter lorsque l'on lance le programme
def Start():
	print("")
	listCoord = []

	files = listdir(sys.argv[1])

	if(len(sys.argv) > 2 and sys.argv[2] == "black"):
	        black = True
	
	for f in files:
		if f.endswith(".jpg") or f.endswith(".png") :
			im = Image.open(sys.argv[1]+"/"+f)
			img = im.convert("RGB")
			radius = calculeSide(img,f)
			image = reconize(img,radius)
			image.save(sys.argv[2]+"/"+"detecte_"+ f)
			G,FP,FN = reussite(f,image)

			listCoord.append(G)
			listCoord.append(FP)
			listCoord.append(FN)


	graph(listCoord)



def graph(listCoord):
	i = 0
	y0 = []
	xGood = 1
	x = []
	while(i < len(listCoord)-2):
		x.append(xGood)
		xGood = xGood + 1
		y0.append(listCoord[i])
		i = i + 3
	plt.plot(x,y0,color = "green", lw = 3, label = "Bon", alpha=0.5)

	i = 1
	y1 = []
	while(i < len(listCoord)-1):
		y1.append(listCoord[i])
		i = i + 3
	plt.plot(x,y1,color = "red", lw = 3, label = "Faux Positif", alpha=0.5)

	i = 2
	y2 = []
	while(i < len(listCoord)):
		y2.append(listCoord[i])
		i = i + 3

	plt.plot(x,y2,color = "blue", lw = 3, label = "Faux Negatif", alpha=0.5)


	plt.title("Total des % de reussites de toutes les images")
	plt.legend(loc='center left')

	plt.xlabel("Images")
	xtick = []
	for j in range(len(listCoord)//3):
		j = j + 1
		xtick.append(j)
	plt.xticks(xtick)

	plt.ylabel("Pourcentage")
	plt.show()
	plt.close()


#Fonction permettant de reconnaître la censure en essaynt de trouver des pixels de même couleurs côte à côte
def reconize(img,side):

	pixR = img.load()
	thumb = img.copy()
	pix = thumb.load()

	list_X = []
	list_Y = []

	#Reconnaître des pixels similaires côte à côte
	for x in range(0,img.size[0]-side, side):


		for y in range(0,img.size[1]-side,side):

			if(pix[x,y] != (0,0,255)):

				cmpt = 0

				for xp in range(x,x+side):
					for yp in range(y,y+side):
						if(soustraction(pixR[xp,yp],pixR[x,y]) <= 5):
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



    #Reconnaître des rectangle à 90% de bleu
	for x in range(0,img.size[0]-side,side):

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


def reussite(f,image):

	print("Resultat")
	print("")

	Good = 0
	FauxNegatif = 0
	FauxPositif = 0
	totGT = 0
	Resolution = image.size[0]*image.size[1]

	print("Resolution : ", Resolution)

	maskGT = Image.new( "L",image.size)
	pixGT = maskGT.load()

	fn = "Coordonnee/"+ f + ".txt"
	for line in open(fn):
		x,y,r = tuple(map(int, line.split()))

		for i in range(x,x+r):
			for j in range(y,y+r):
				pixGT[i,j] = 255
	#maskGT crée (mask vrai)

	pix = image.load()
	maskRes = Image.new( "L",image.size)
	pixRes = maskRes.load()
	
	for x in range(image.size[0]):
		for y in range(image.size[1]):
			if(pix[x,y] == (0,0,255)):
				pixRes[x,y] = 200
			#Calcul du total des pixels blanc du maskGT (pour calcul des % après)
			if(pixGT[x,y] == 255):
				totGT = totGT + 1
	#maskRes crée (mask que le programme trouve)

	print("réel : ", totGT)


	maskFinal = Image.new("RGB",image.size)
	pixfinal = maskFinal.load()
	for x in range(image.size[0]):
		for y in range(image.size[1]):

			#Bon
			if(pixRes[x,y] == 200 and pixGT[x,y] == 255):
				pixfinal[x,y] = 0,255,0
				Good = Good +1

			#FauxPositif
			if(pixRes[x,y] == 200 and pixGT[x,y] == 0):
				pixfinal[x,y] = 255,0,0
				FauxPositif = FauxPositif +1

			#FauxNégatif
			if(pixRes[x,y] == 0 and pixGT[x,y] == 255):
				pixfinal[x,y] = 255,192,203
				FauxNegatif = FauxNegatif+1

	maskFinal.show()
	print("programme : ", Good)
	
	#Revoir calculs
	percentGood = abs((float) (Good/totGT)*100)
	percentFauxPositif = abs((float) (FauxPositif/(Resolution))*100)
	percentFauxNegatif = abs((float) (percentGood - 100))

	print(""+f + " positif = " , percentGood , " %")
	print(""+f + " Faux Positif = " , percentFauxPositif , " %")
	print(""+f + " Faux Negatif = " , percentFauxNegatif , " %")
	print("")
	print("")


	#Histograme
	s = pd.Series(
		[percentGood, percentFauxPositif, percentFauxNegatif],
		index = ["Good", "FP", "FN"]
	)

	#Set descriptions:
	plt.title("% de reussite de detection de : "+f)
	plt.ylabel('Pourcentage')

	#Set tick colors:
	ax = plt.gca()
	ax.tick_params(axis='x', colors='blue')
	ax.tick_params(axis='y', colors='black')

	#Plot the data:
	my_colors = ['green','red','blue']  #green, red, blue

	s.plot( 
	kind='bar', 
	color=my_colors,
	)

	#Si on veut un diagramme pour chaque photo
	#plt.show()
	plt.close()

	return (percentGood,percentFauxPositif,percentFauxNegatif)


#Fonction permettant la soustraction entre 2 pixels
def soustraction(pix1, pix2):

	R1,G1,B1 = pix1
	R2,G2,B2 = pix2
	
	#calcul soustraction
	R = abs(R1-R2)
	G = abs(G1-G2)
	B = abs(B1-B2)
	
	#pix3 = R,G,B
	total = R+G+B
	
	#return pix3
	return total

Start()
