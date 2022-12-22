import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

import mysql.connector
from mysql.connector import Error

connection_config = {
    "host" : "localhost",
    "user" :"py",
    "password":"python",
    "auth_plugin" : "mysql_native_password",
    "database" : "Allocine",
    "port" : "3308"        
}

id_film = '61282' # mettre l'id du film, trouvable dans l'URL

def note_sql(User, Note):
    
    try :
        mydb = mysql.connector.connect(**connection_config)
        mycursor = mydb.cursor()
        sql = f"""INSERT INTO notes (`ID`, `User`, `Note`) VALUES ('1','{User}','{Note}');"""      
        mycursor.execute(sql)
        mydb.commit()
        print(mycursor.rowcount, f"record inserted.")
        return True

    except Error as e:
        print(f"ça marche pas, parce que : {e}")
        return False

    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed")


def url_set():
    
    i=1

    global soup

    while True:
        i=i+1
        
        try:
            url = f"""https://www.allocine.fr/film/fichefilm-{id_film}/critiques/spectateurs/?page={i}"""
            req = requests.get(url)
            soup = BeautifulSoup(req.content)
            print(scrap())
            list_note = scrap()
            for x in list_note:
                note_sql(x, list_note[x])

        except:
            print("NOK")
            return False


def scrap():
    
    n_n = {}

    for link in soup.find_all('div', {"class": "hred review-card cf"}):
        str_link = BeautifulSoup(str(link))
        # print(str_link)
        
        try:
            name = (str_link.select_one("figure", class_='thumbnail', ).select_one("span").attrs["title"])
            note = (str_link.find("span", class_="stareval-note").text).replace(",",".")
            n_n[name]=note

        except:
            pass

    return n_n

url_set()