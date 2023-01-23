import mysql.connector as mysqlpy
from util import standardize_phrase, predict_com, web_scrapping, titre_film_allocine, enlever_espace_debut_fin
from flask import Flask, render_template, redirect, request, flash, jsonify


coms_db = {'user': 'root',
           'password': 'example',
           'host': 'localhost',
           'port': '3308',
           'database': 'com_testés'}
  
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
  
#adresse tuto: https://www.geeksforgeeks.org/how-to-connect-reactjs-with-flask-api/ 

@app.route('/analyse', methods=['POST'])
def analyse():
    if request.method == 'POST':
        data = request.get_json()
        commentaire = data['commentaire']

        bool = ''
        proba = ''

        if len(commentaire) == 0:
            flash('Votre commentaire est trop court !!')
        else:
            standard = standardize_phrase(commentaire)
            predict = predict_com(standard)

            if predict[0][0] == 0:
                bool = False
            elif predict[0][0] == 1:
                bool = True

            if predict[1][0][0] > predict[1][0][1]:
                proba = f'''Je suis sûr à {round(predict[1][0][0] * 100, 2)} que le commentaire est négatif !'''
            elif predict[1][0][1] > predict[1][0][0]:
                proba = f'''Je suis sûr à {round(predict[1][0][1] * 100, 2)} que le commentaire est positif !'''

            bdd = mysqlpy.connect(user=coms_db["user"], password=coms_db["password"],
                                  host=coms_db["host"], port=coms_db["port"], database=coms_db["database"])
       
            cursor = bdd.cursor()
            cursor.execute(
                f'''INSERT INTO commentaires (commentaire, avis_model_IA)
                VALUES("{enlever_espace_debut_fin(commentaire.replace('"', ""))}", "{float(predict[0])}");''')
            bdd.commit()

            cursor.execute(f'''SELECT id FROM commentaires WHERE commentaire = "{enlever_espace_debut_fin(commentaire.replace('"', ''))}";''')
            id = cursor.fetchone()

            cursor.close()
            bdd.close()
   
            response = [{
                'commentaire': commentaire.replace('"', ""),
                'like': bool,
                'proba': proba,
                'id': id[0]
            }]

            bdd.close()

        return jsonify(response)

@app.route('/analyse/sentiment', methods=['PUT'])
def upgrade():
    if request.method == 'PUT':
            data = request.get_json()
            sentiment = data['sentiment']
            id = data['id']
           
            bdd = mysqlpy.connect(user=coms_db["user"], password=coms_db["password"],
                                  host=coms_db["host"], port=coms_db["port"], database=coms_db["database"])
              

            cursor = bdd.cursor()
            cursor.execute(f'''UPDATE commentaires SET avis_perso = "{sentiment}" WHERE id = {id};''')
            bdd.commit()
            cursor.close()
            bdd.close()

            return jsonify({'message': 'Modification réalisée !'})
        

    
@app.route('/archives', methods=['GET'])
def archives():
    if request.method == 'GET':
        bdd = mysqlpy.connect(user=coms_db["user"], password=coms_db["password"],
                                  host=coms_db["host"], port=coms_db["port"], database=coms_db["database"])
       
        cursor = bdd.cursor()
        cursor.execute(
            f'''SELECT * FROM commentaires ORDER BY date DESC;''')
        commentaires = cursor.fetchall()

        commentaires_list = []
        for commentaire in commentaires:
            commentaires_list.append({
                "id": commentaire[0],
                "date": commentaire[1],
                "commentaire": commentaire[2],                
                "sentiment": commentaire[4],
                "avis_IA": commentaire[3]
            })

        cursor.close()
        bdd.close()

        return jsonify(commentaires_list)

@app.route('/scrapping/commentaires', methods=['POST'])
def scrapping():
    if request.method == 'POST':
        data = request.get_json()
        num_film = data['numFilm']
        titre_film = titre_film_allocine(num_film)     
        
        commentaires = web_scrapping(num_film)

        commentaires_titre = {
            'titre': titre_film,
            'commentaires': commentaires
        }

        return jsonify(commentaires_titre)

if __name__ == '__main__':
    app.run(debug=True)

#code pour lancer le serveur sans devoir le redémarrer à chaque fois : flask --app server.py --debug run