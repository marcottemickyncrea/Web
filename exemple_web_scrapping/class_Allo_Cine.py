from bs4 import BeautifulSoup
import requests
import re
import mysql.connector as pymysql

#r = requests.get("https://www.barreaudenice.com/annuaire/avocats/")
#print(r.status_code)


class Allo_Cine :
    @staticmethod
    def get_all_pages():
        urls = []
        page_number = 1
        for i in range(667):
            i = f"https://www.allocine.fr/film/fichefilm-61282/critiques/spectateurs/?page={page_number}"
            page_number += 1
            urls.append(i)
            #print(urls)
        return urls

    @staticmethod
    def parse_avis(url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        #print(soup)
        avis = soup.find_all('div', class_='review-card-review-holder')
        
        for av in avis:
            try:
                commentaires = av.find("div", class_="content-txt review-card-content").text.strip()
            except AttributeError as e:
                commentaires = ""
            try:    
                notes = av.find("span",class_="stareval-note").text.strip()
            except AttributeError as e:
                notes = ""

            
            


            # chemin = "/home/diaby/IA_dev_Python/py-sql/webScraping/annuaire_avocats.txt"
            # with open(chemin, "a") as f:
            #     f.write(f"{nom}\n")
            #     f.write(f"{adresse_finale}\n")
            #     f.write(f"{tel}\n")
            #     f.write(f"{email}\n\n")

                # Connexion BDD

            mydb = pymysql.connect(
                                    host="localhost",
                                    user="root",
                                    password="example",
                                    database="AlloCine",
                                    port = 3307
                                    )
            mycursor = mydb.cursor()

            # Insertion BDD
            sql = f"""INSERT INTO allocine (commentaires, notes) VALUES ("{commentaires.replace('"',' ')}", "{notes.replace(',','.')}")"""
            mycursor.execute(sql)
            print(sql)
            mydb.commit()
            
    @staticmethod
    def parse_all_avis():
        pagees = Allo_Cine.get_all_pages()

        for page in pagees:
            Allo_Cine.parse_avis(url=page)
            print(f"on scrape {page}")



avis = Allo_Cine.parse_all_avis()