# coding: utf-8

### BONJOUR, ICI Jean-Hugues ###
### Comme toujours, mes notes et corrections sont précédées de trois dièses ###

import csv
import requests
from bs4 import BeautifulSoup
fichier = "moisson-cellulaire.csv"

for n in range (1,101):
	url = "https://www.kijiji.ca/b-cellulaire/ville-de-montreal/page-{}/c760l1700281".format(n)
	
	contenu = requests.get(url) 
	page = BeautifulSoup(contenu.text,"html.parser")

	url_des_cells = page.find_all("div", class_="title")
	
	for url_cell in url_des_cells:
		
		try:
			cell = []
			url2 = url_cell.a["href"]
			
			url2 = "https://www.kijiji.ca" + url2
			
			cell.append(url2)

			contenu2 = requests.get(url2)
			page2 = BeautifulSoup(contenu2.text,"html.parser")

		
			titre = page2.title.text.split("|")[0].strip()
			
			cell.append(titre)

#Ici je veux isoler le prix et le mettre en nombre pour que je puisse éventuellement ajouter un grade de couleur pour chaque tranche de prix dans ma carte

### La ligne ci-dessous était mal indentée et ton script ne fonctionnait pas...

      # prix = page2.find("span", class_="currentPrice-2872355490").text
			prix = page2.find("span", class_="currentPrice-2872355490").text
			prix = prix.strip("$") ### C'est vrai, voilà une autre application pratique de la fonction .strip()!
			prix = prix.replace(",", ".")
			
			try:
				prix = float(prix)
			except:
				prix = "Échange ou sur demande"

			cell.append(prix)
      
#Ici je veux récupérer les données géographiques de l'annonce pour pouvoir répertorier où l'appareil est disponible sur une carte

### La ligne ci-dessous était elle aussi mal indentée et ton script ne fonctionnait pas...
      # infos = page2.find_all("dt")
			infos = page2.find_all("dt")
			latitude = page2.find("meta",attrs={"property":"og:latitude"})["content"]
			
			cell.append(latitude)

			longitude = page2.find("meta",attrs={"property":"og:longitude"})["content"]
		
			cell.append(longitude)

			print(cell)
      
#je crée un fichier CSV pour me permettre d'avoir un fichier qui pourra être vu par l'application Fusion Tables de Google
### Un CSV peut être aussi lu par tout logiciel tableur comme Excel, Calc de LibreOffice ou OpenOffice, ou encore les feuilles de calcul Google
			
### Même chose pour la ligne ci-dessous; sa mauvaise indentation empêchait ton script de fonctionner...
      # f = open(fichier,"a")
			f = open(fichier,"a")
			nouvelle_variable = csv.writer(f)
			nouvelle_variable.writerow(cell)

		except:
			print("Donnée non disponible")

### Très cool!
### Une fois les indentations corrigées, ça fonctionne très bien!
### Je serais aussi allé chercher la date de l'annonce.