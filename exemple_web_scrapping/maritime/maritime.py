from bs4 import BeautifulSoup
import requests
import pandas as pd

class Company():
    """
    Gathers informations about companies such as name, email or website.
    Its methods enable to save infos in a database as well as in an excel file.
    Moreover the send_email() static method can send a email to all the companies
    """
    def __init__(self,
                 name: str,
                 description: str,
                 website: str,
                 email: str,
                 address: str,
                 contactName: str) -> None:
        self.name = name
        self.description = description
        self.website = website
        self.email = email
        self.address = address
        self.contactName = contactName

    @staticmethod
    def retrieve_companies_pages() -> list[str]:
        """
        Get companies url from https://www.normandie-maritime.fr/annuaire-activites-maritimes.html
        and return them as a list
        """
        companies_links = []
        page = requests.get(f"https://www.normandie-maritime.fr/annuaire-activites-maritimes.html")
        soup = BeautifulSoup(page.content, 'html.parser')

        # On recupere l'url des pages d'informations des entreprises
        companies = soup.find_all("a", class_="infosOrganisme")
        
        for company in companies:
            #print(company['href'])
            companies_links.append(company['href'])
        
        return companies_links

    @staticmethod
    def get_companies_infos(companies_links: list["Company"]) -> list:
        try:
            """
            Retrieves infos about companies and returns a list of dictionaries
            """

            companies_list = []

            for companies_link in companies_links:
                information_page = requests.get(f"https://www.normandie-maritime.fr/{companies_link}")
                information_soup = BeautifulSoup(information_page.content, 'html.parser')

                #name
                name = information_soup.find("p",  class_="titre").text

                #description
                try:
                    #description = information_soup.find("p",  attrs={'style' : 'text-align: left;'}).text
                    description = information_soup.find("div",  class_ = "detailsTexte").text.replace("\n", "")

                except:
                    description = "NaN"

                #website
                try:
                    website = information_soup.find("a",  class_="detailsIcon url")['href']

                except:
                    website = "NaN"

                #email
                container = information_soup.find("p", class_="detailsIcon email")
                mailto = container.findChildren("a" , recursive=False)
                email = ""
                for element in mailto:
                    email = element['href'].replace("mailto:", "")
                    if email == "":
                        email = "NaN"

                #address
                address = information_soup.find("p",  class_="detailsIcon adresse").text

                #contactName
                contactName = information_soup.find("p",  class_="detailsIcon nomContact").text

                company = Company(name, description, website, email, address, contactName)

                companies_dict = {
                    "name" : company.name,
                    "description" : company.description,
                    "website" : company.website,
                    "email" : company.email,
                    "contactName" : company.contactName
                }
                companies_list.append(companies_dict)

            print("done")
            return companies_list
        
        except:
            print("there's a problem houston")  
            return ""

if __name__ == "__main__":

    liste_societes_maritime = Company.retrieve_companies_pages()
    infos_societes_maritimes = Company.get_companies_infos(liste_societes_maritime)
    
    for company in infos_societes_maritimes:
        print(company)