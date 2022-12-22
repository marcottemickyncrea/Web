from flask import render_template, request, redirect, url_for
from app import app
from .db import get_db_config, db_connect
import mysql.connector
from bs4 import BeautifulSoup
import requests


# Afficher les valeurs utilisateurs dans le tableau puis db
# Mettre le cemin absolu de votre config.json
path = "/home/kevin/workspace/py-sql/flask/app_mega_tutorail/app_ensemble/config.json"
config = get_db_config(path)

myDB = db_connect(config)
cursor = myDB.cursor()
dbOK = myDB.is_connected()

@app.route('/')

@app.route('/index', methods=["GET", "POST"])   # == @app.route('/index')
def index():

    if request.method == "GET":

        try:
            query="""
                SELECT * FROM `Utilisateur`;
            """
            cursor.execute(query)
            result_select = cursor.fetchall()

            return render_template('index.html',configHTML=config, dbOK__=dbOK, HTML_Result=result_select)
        

        except mysql.connector.Error as e:
            return render_template('index.html', configHTML=config, error=e)

        # inserer des valeurs utilisateurs dans le tableau puis db

    if request.method == "POST":

        try:
            prenom = request.form["prenom"]
            nom = request.form["nom"]
            adresse_mail = request.form["adresse_mail"]

            query=f"""
                INSERT INTO Utilisateur (nom, prenom, adresse_email) VALUES ("{nom}", "{prenom}", "{adresse_mail}");
            """
            cursor.execute(query)
            myDB.commit()
            
            return redirect(url_for("index"))

        except mysql.connector.Error as e:
            return redirect(url_for("index"), error=e)


@app.route('/tesla', methods=['GET', 'POST'])   # == @app.route('/index')
def tesla():
    if request.method == "GET":
        try:
        

            
            query="""
                SELECT * FROM tesla;
            """
            cursor.execute(query)
            result_select = cursor.fetchall()

            return render_template('tesla.html', HTML_Result=result_select)
    
        except mysql.connector.Error as e:
            return render_template('tesla.html')


          
    if request.method == 'POST':

        try :
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
            myDB.commit()
            return redirect(url_for("tesla"))
            
        except mysql.connector.Error as e:
            return render_template('tesla.html')
    
    
        


    


        
   