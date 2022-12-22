from flask import render_template, request, redirect, url_for, flash
from app import app

import mysql.connector as mysqlpy

user = 'root'
password = 'example'
host = 'localhost'
port = '3308'
database = 'tesla'

@app.route('/')
def destinations():
    bdd = mysqlpy.connect(user=user, password=password,
                      host=host, port=port, database=database)
    cursor = bdd.cursor()
    cursor.execute('SELECT * FROM voitures;')
    voitures = cursor.fetchall()
    cursor.close()
    bdd.close()
    
    return render_template('index.html', voitures=voitures)