from flask import jsonify, request
from server_flask import app

import mysql.connector as mysqlpy

musics_db = {'user': 'root',
        'password': 'example',
        'host': 'localhost',
        'port': '3308',
        'database': 'API REST'}

@app.route('/api/musics/<int:id>', methods=['GET'])
def get_musics(id): 
    print(id)   
    if request.method == 'GET':  
        bdd = mysqlpy.connect(user=musics_db["user"], password=musics_db["password"],
                        host=musics_db["host"], port=musics_db["port"], database=musics_db["database"])      
        cursor = bdd.cursor()
        cursor.execute(f'''SELECT id, name, artist FROM musics WHERE id = {id};''')
        music = cursor.fetchone()
    

        music_one = [{'id': music[0], 'name':music[1], 'artist':music[2]}]

        cursor.close()
        bdd.close()
        return jsonify(music_one)

@app.route('/api/musics/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def musics():    
    if request.method == 'GET':  
        bdd = mysqlpy.connect(user=musics_db["user"], password=musics_db["password"],
                        host=musics_db["host"], port=musics_db["port"], database=musics_db["database"])      
        cursor = bdd.cursor()
        cursor.execute('SELECT id, name, artist FROM musics;')
        musics = cursor.fetchall()
    
        music_list = []
        for music in musics:
            music_list.append({'id': music[0], 'name':music[1], 'artist':music[2]})

        cursor.close()
        bdd.close()
        return jsonify(music_list)

    if request.method == 'POST':  
        bdd = mysqlpy.connect(user=musics_db["user"], password=musics_db["password"],
                        host=musics_db["host"], port=musics_db["port"], database=musics_db["database"]) 
        data= request.get_json()

        cursor = bdd.cursor()
        cursor.execute(
            f'''INSERT INTO musics (name, artist)
            VALUES("{data['name']}", "{data['artist']}");''')
        bdd.commit()
        # result_db = musics()
        cursor.close()
        bdd.close()  
  
        #return result_db
        return jsonify({'message': 'Nouveau commentaire ajouté !'})
    
    if request.method == 'PUT':
        bdd = mysqlpy.connect(user=musics_db["user"], password=musics_db["password"],
                        host=musics_db["host"], port=musics_db["port"], database=musics_db["database"]) 
        data= request.get_json()        

        cursor = bdd.cursor()
        cursor.execute(f'''UPDATE musics SET artist = "{data['artist']}" WHERE id = {data['id']};''')
        bdd.commit()
        cursor.close()
        bdd.close()

        return jsonify({'message': 'Modification réalisée !'})

    if request.method == 'DELETE':
        bdd = mysqlpy.connect(user=musics_db["user"], password=musics_db["password"],
                        host=musics_db["host"], port=musics_db["port"], database=musics_db["database"]) 
        data= request.get_json()

        cursor = bdd.cursor()
        cursor.execute(f'''DELETE FROM musics WHERE id = {data['id']};''')
        bdd.commit()
        cursor.close()
        bdd.close()

        return jsonify({'message': 'Suppression réalisée !'})

coms_db = {'user': 'root',
        'password': 'example',
        'host': 'localhost',
        'port': '3308',
        'database': 'allociné'}

@app.route('/api/commentaires/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def commentaires():    
    if request.method == 'GET':  
        bdd = mysqlpy.connect(user=coms_db["user"], password=coms_db["password"],
                        host=coms_db["host"], port=coms_db["port"], database=coms_db["database"])      
        cursor = bdd.cursor()
        cursor.execute('SELECT id_commentaire, note, commentaire FROM avatar1;')
        coms = cursor.fetchall()
    
        coms_list = []
        for com in coms:
            coms_list.append({'id': com[0], 'note':com[1], 'commentaire':com[2]})

        cursor.close()
        bdd.close()
        return jsonify(coms_list)

    if request.method == 'POST':  
        bdd = mysqlpy.connect(user=coms_db["user"], password=coms_db["password"],
                        host=coms_db["host"], port=coms_db["port"], database=coms_db["database"])  
        data= request.get_json()

        cursor = bdd.cursor()
        cursor.execute(
            f'''INSERT INTO avatar1 (note, commentaire)
            VALUES("{data['note']}", "{data['commentaire']}");''')
        bdd.commit()
        cursor.close()
        bdd.close()  
  
        return jsonify({'message': 'Nouveau commentaire ajouté !'})
    
    if request.method == 'PUT':
        bdd = mysqlpy.connect(user=coms_db["user"], password=coms_db["password"],
                        host=coms_db["host"], port=coms_db["port"], database=coms_db["database"])  
        data= request.get_json()        

        cursor = bdd.cursor()
        cursor.execute(f'''UPDATE avatar1 SET commentaire = "{data['commentaire']}" WHERE id_commentaire = {data['id']};''')
        bdd.commit()
        cursor.close()
        bdd.close()

        return jsonify({'message': 'Modification réalisée !'})

    if request.method == 'DELETE':
        bdd = mysqlpy.connect(user=coms_db["user"], password=coms_db["password"],
                        host=coms_db["host"], port=coms_db["port"], database=coms_db["database"])  
        data= request.get_json()

        cursor = bdd.cursor()
        cursor.execute(f'''DELETE FROM avatar1 WHERE id_commentaire = {data['id']};''')
        bdd.commit()
        cursor.close()
        bdd.close()

        return jsonify({'message': 'Suppression réalisée !'})

@app.route('/api/fleurs/<int:id>', methods=['GET'])
def get_fleur(id): 
    if request.method == 'GET':  
        bdd = mysqlpy.connect(user=musics_db["user"], password=musics_db["password"],
                        host=musics_db["host"], port=musics_db["port"], database=musics_db["database"])      
        cursor = bdd.cursor()
        cursor.execute(f'''SELECT id_fleur, nom, provenance FROM fleurs WHERE id_fleur = {id};''')
        fleur = cursor.fetchone()
    

        fleur_one = [{'id': fleur[0], 'nom':fleur[1], 'provenance':fleur[2]}]

        cursor.close()
        bdd.close()
        return jsonify(fleur_one)

@app.route('/api/fleurs/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def fleurs():    
    if request.method == 'GET':  
        bdd = mysqlpy.connect(user=musics_db["user"], password=musics_db["password"],
                        host=musics_db["host"], port=musics_db["port"], database=musics_db["database"])      
        cursor = bdd.cursor()
        cursor.execute('SELECT id_fleur, nom, provenance FROM fleurs;')
        fleurs = cursor.fetchall()
    
        fleurs_list = []
        for fleur in fleurs:
            fleurs_list.append({'id': fleur[0], 'nom':fleur[1], 'provenance':fleur[2]})

        cursor.close()
        bdd.close()
        return jsonify(fleurs_list)

    if request.method == 'POST':  
        bdd = mysqlpy.connect(user=musics_db["user"], password=musics_db["password"],
                        host=musics_db["host"], port=musics_db["port"], database=musics_db["database"]) 
        data= request.get_json()

        cursor = bdd.cursor()
        cursor.execute(
            f'''INSERT INTO fleurs (nom, provenance)
            VALUES("{data['nom']}", "{data['provenance']}");''')
        bdd.commit()
        # result_db = musics()
        cursor.close()
        bdd.close()  
  
        #return result_db
        return jsonify({'message': 'Nouvelle(s) fleur(s) ajoutée(s) !'})
    
    if request.method == 'PUT':
        bdd = mysqlpy.connect(user=musics_db["user"], password=musics_db["password"],
                        host=musics_db["host"], port=musics_db["port"], database=musics_db["database"]) 
        data= request.get_json()        

        cursor = bdd.cursor()
        cursor.execute(f'''UPDATE fleurs SET nom = "{data['nom']}" WHERE id_fleur = {data['id']};''')
        bdd.commit()
        cursor.close()
        bdd.close()

        return jsonify({'message': 'Modification réalisée !'})

    if request.method == 'DELETE':
        bdd = mysqlpy.connect(user=musics_db["user"], password=musics_db["password"],
                        host=musics_db["host"], port=musics_db["port"], database=musics_db["database"]) 
        data= request.get_json()

        cursor = bdd.cursor()
        cursor.execute(f'''DELETE FROM fleurs WHERE id_fleur = {data['id']};''')
        bdd.commit()
        cursor.close()
        bdd.close()

        return jsonify({'message': 'Suppression réalisée !'})

@app.route('/api/animaux/<int:id>', methods=['GET'])
def get_animal(id): 
    print(id)   
    if request.method == 'GET':  
        bdd = mysqlpy.connect(user=musics_db["user"], password=musics_db["password"],
                        host=musics_db["host"], port=musics_db["port"], database=musics_db["database"])      
        cursor = bdd.cursor()
        cursor.execute(f'''SELECT id_animal, nom, provenance FROM animaux WHERE id_animal = {id};''')
        animal = cursor.fetchone()
    

        animal_one = [{'id': animal[0], 'nom':animal[1], 'provenance':animal[2]}]

        cursor.close()
        bdd.close()
        return jsonify(animal_one)

@app.route('/api/animaux/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def animaux():    
    if request.method == 'GET':  
        bdd = mysqlpy.connect(user=musics_db["user"], password=musics_db["password"],
                        host=musics_db["host"], port=musics_db["port"], database=musics_db["database"])      
        cursor = bdd.cursor()
        cursor.execute('SELECT id_animal, nom, provenance FROM animaux;')
        animaux = cursor.fetchall()
    
        animaux_list = []
        for animal in animaux:
            animaux_list.append({'id': animal[0], 'nom':animal[1], 'provenance':animal[2]})

        cursor.close()
        bdd.close()
        return jsonify(animaux_list)

    if request.method == 'POST':  
        bdd = mysqlpy.connect(user=musics_db["user"], password=musics_db["password"],
                        host=musics_db["host"], port=musics_db["port"], database=musics_db["database"]) 
        data= request.get_json()

        cursor = bdd.cursor()
        cursor.execute(
            f'''INSERT INTO animaux (nom, provenance)
            VALUES("{data['nom']}", "{data['provenance']}");''')
        bdd.commit()
        # result_db = musics()
        cursor.close()
        bdd.close()  
  
        #return result_db
        return jsonify({'message': 'Nouvelle(s) animal(s) ajoutée(s) !'})
    
    if request.method == 'PUT':
        bdd = mysqlpy.connect(user=musics_db["user"], password=musics_db["password"],
                        host=musics_db["host"], port=musics_db["port"], database=musics_db["database"]) 
        data= request.get_json()        

        cursor = bdd.cursor()
        cursor.execute(f'''UPDATE animaux SET nom = "{data['nom']}" WHERE id_animal = {data['id']};''')
        bdd.commit()
        cursor.close()
        bdd.close()

        return jsonify({'message': 'Modification réalisée !'})

    if request.method == 'DELETE':
        bdd = mysqlpy.connect(user=musics_db["user"], password=musics_db["password"],
                        host=musics_db["host"], port=musics_db["port"], database=musics_db["database"]) 
        data= request.get_json()

        cursor = bdd.cursor()
        cursor.execute(f'''DELETE FROM animaux WHERE id_animal = {data['id']};''')
        bdd.commit()
        cursor.close()
        bdd.close()

        return jsonify({'message': 'Suppression réalisée !'})