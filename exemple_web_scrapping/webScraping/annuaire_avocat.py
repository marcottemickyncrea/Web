from bs4 import BeautifulSoup
import requests
import re
import mysql.connector as pymysql

#r = requests.get("https://www.barreaudenice.com/annuaire/avocats/")
#print(r.status_code)

def get_all_pages():
    urls = []
    page_number = 1
    for i in range(104):
        i = f"https://www.barreaudenice.com/annuaire/avocats/{page_number}"
        page_number += 1
        urls.append(i)
        #print(urls)
    return urls


def parse_attorney(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    #print(soup)
    attorneys = soup.find_all('div', class_='callout secondary annuaire-single')
    
    for attorney in attorneys:
        try:
            nom = attorney.find("h3").text.strip()
        except AttributeError as e:
            nom = ""
        try:    
            adresse = attorney.find("span",class_="adresse").text.strip()
        except AttributeError as e:
            adresse = ""

        try:
            adresse_finale = re.sub(r"\s+", " ", adresse)
        except AttributeError as e:
            adresse_finale = ""

        try:    
            tel = attorney.find("span", class_="telephone").text.strip()
        except AttributeError as e:
            tel = ""

        try:
            email = attorney.find("span", class_="email").a.text.strip()
        except AttributeError as e:
            email = ""
        


        chemin = "/home/diaby/IA_dev_Python/py-sql/webScraping/annuaire_avocats.txt"
        with open(chemin, "a") as f:
            f.write(f"{nom}\n")
            f.write(f"{adresse_finale}\n")
            f.write(f"{tel}\n")
            f.write(f"{email}\n\n")

            # Connexion BDD

        mydb = pymysql.connect(
                                host="localhost",
                                user="root",
                                password="example",
                                database="Avocats",
                                port = 3307
                                )
        mycursor = mydb.cursor()

        # Insertion BDD
        sql = f"""INSERT INTO infos_avocat (nom, adresse,telephone,email) VALUES ("{nom}", "{adresse_finale}","{tel}","{email}")"""
        mycursor.execute(sql)

        mydb.commit()

       

        

def parse_all_attorney():
    pagees = get_all_pages()

    for page in pagees:
        parse_attorney(url=page)
        print(f"on scrape {page}")




parse_all_attorney()
