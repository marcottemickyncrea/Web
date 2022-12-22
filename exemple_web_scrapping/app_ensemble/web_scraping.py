from bs4 import BeautifulSoup
import requests
import pandas as pd
import mysql.connector as mysqlpy
# ---------------------------------------------------------------------
# Accés à la bdd
#-----------------------------------------------------------------------------------
user = 'root'
password = 'example'
host = 'localhost'
port = '3307'
database = 'flask_tuto'

bdd = mysqlpy.connect(user=user, password=password, host=host, port=port, database=database)
cursor = bdd.cursor()


pages = ["models","model3","modelx"]


for page in pages:
    url = f"https://www.tesla.com/fr_fr/{page}"
    reponse=requests.get(url)
    soup = BeautifulSoup(reponse.text,"html.parser")
    donnees=soup.find_all("div", {"class": "tcl-badge__primary-copy tds-text--h2"})

    nom_voiture = page
    autonomie = donnees[0].text.replace("\n","").replace(" ","")
    acceleration = donnees[1].text.replace("\n","").replace(" ","")
    vitesse_max = donnees[2].text.replace("\n","").replace(" ","")
    puissance = donnees[3].text.replace("\n","").replace(" ","")

    print(page, autonomie, acceleration, vitesse_max, puissance)
    query =f"""INSERT INTO tesla(nom_voiture, autonomie, acceleration, vitesse_max, puissance) """
    query += f"""VALUES ('{nom_voiture}','{autonomie}','{acceleration}','{vitesse_max}','{puissance}')"""
    cursor.execute(query)
bdd.commit()
cursor.close()
bdd.close()

