from flask import Flask, request,render_template
import mysql.connector as pymysql

try: 
    mydb = pymysql.connect(
                                host="localhost",
                                user="root",
                                password="example",
                                database="Avocats",
                                port = 3307
                                )
except:
    print ("Impossible de se connecter à la base, veillez checker la chaine de connexion.")
mycursor = mydb.cursor()


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/avocats')
def avocats():
    mycursor.execute("SELECT * FROM infos_avocat")
    data = mycursor.fetchall()
    return render_template('avocats.html', data=data)