from flask import render_template, request, redirect, url_for, flash
from app import app

import mysql.connector as mysqlpy

user = 'root'
password = 'example'
host = 'localhost'
port = '3308'
database = 'airbnb'

'''bdd = mysqlpy.connect(user=user, password=password,
                      host=host, port=port, database=database)
cursor = bdd.cursor()'''

@app.route('/index')
def destinations():
    bdd = mysqlpy.connect(user=user, password=password,
                      host=host, port=port, database=database)
    cursor = bdd.cursor()
    cursor.execute('SELECT * FROM destinations;')
    destinations = cursor.fetchall()
    cursor.close()
    bdd.close()
    response = False
    fichier = 'index.html'
    if response:
        fichier = 'index.html'
    else:
        fichier='index copy.html'

    return render_template(fichier, destinations = destinations)

@app.route('/ajout-destination', methods= ['GET', 'POST'])
def ajouter_destination():
    if request.method == 'POST':
        bdd = mysqlpy.connect(user=user, password=password,
                      host=host, port=port, database=database)
        cursor = bdd.cursor()
        url_image = request.form['url-image']        
        adresse_destination = request.form['localisation']
        type_destination = request.form['type']
        dates = request.form['dates']
        prix_destination = request.form['prix']
        note_destination = 0
        query=f'''INSERT INTO destinations(url_image, adresse_destination, type_destination, dates, prix_destination, note_destination) 
                VALUES({url_image}, {adresse_destination}, {type_destination}, {dates}, {prix_destination}, 'note_destination');'''
        cursor.execute(query)
        bdd.commit() 
        cursor.close()
        bdd.close()
        return redirect('index')
    return render_template('ajout-destination.html')

@app.route('/modifier-destination', methods = ['GET', 'POST'])
def modifier_destination():
    if request.method == 'POST':
        bdd = mysqlpy.connect(user=user, password=password,
                      host=host, port=port, database=database)
        cursor = bdd.cursor()

        id_destination = request.form['id']
        url_image = request.form['url-image']        
        adresse_destination = request.form['localisation']
        type_destination = request.args['type']
        dates = request.form['dates']
        prix_destination = request.form['prix']
        note_destination = 0

        querys = []
        if url_image != '':
            querys.append('url_image = "{}"'.format(url_image))
        if adresse_destination != '':
            querys.append('adresse_destination = "{}"'.format(adresse_destination))
        if type_destination != '':
            querys.append('type_destination = "{}"'.format(type_destination))
        if dates != '':
            querys.append('dates = "{}"'.format(dates))
        if prix_destination != '':
            querys.append('prix_destination = "{}"'.format(prix_destination))
        if note_destination != '':
            querys.append('note_destination = "{}"'.format(note_destination))
        join = ', '.join(querys)

        cursor.execute(f'UPDATE destinations SET {join} WHERE id_destination = {id_destination};')
        bdd.commit() 
        cursor.close()
        bdd.close()
        return redirect('index')
    return render_template('modifier-destination.html')

@app.route('/supprimer-destination', methods=['POST', 'GET'])
def supprimer_destination():
    if request.method == 'POST':
        bdd = mysqlpy.connect(user=user, password=password,
                      host=host, port=port, database=database)
        cursor = bdd.cursor()
        id_destination = request.form['id']
        query=f'''DELETE FROM destinations WHERE id_destination={id_destination};'''
        cursor.execute(query)
        bdd.commit()
        cursor.close()
        bdd.close()
        return redirect('index')
    return render_template('supprimer-destination.html')
        
