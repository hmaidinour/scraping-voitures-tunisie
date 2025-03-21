from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3
from datetime import datetime

# URL de base
BASE_URL = 'https://www.automobile.tn/fr/occasion?page={}'
# Listes pour stocker les données
Name, Mileage, Year, Gearbox, Transmission, Horse_Power, Energie, Location, Price, Dates = [], [], [], [], [], [], [], [], [], []

# Connexion à la base SQLite
def get_db_connection():
    conn = sqlite3.connect("annonces.db")
    conn.row_factory = sqlite3.Row
    return conn

# Création de la table si elle n'existe pas
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS annonces (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT, mileage TEXT, year TEXT, gearbox TEXT,
                        transmission TEXT, horsepower TEXT, energie TEXT,
                        location TEXT, price TEXT, date TEXT)''')
    conn.commit()
    conn.close()

init_db()



# Fonction pour insérer une annonce en base
def save_to_db(name, mileage, year, gearbox, transmission, horsepower, energie, location, price, date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO annonces (name, mileage, year, gearbox, transmission, horsepower, energie, location, price, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (name, mileage, year, gearbox, transmission, horsepower, energie, location, price, date))
    conn.commit()
    conn.close()

# Fonction pour récupérer les annonces depuis la base
def fetch_annonces():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM annonces")
    rows = cursor.fetchall()
    conn.close()
    return pd.DataFrame(rows, columns=["id", "name", "mileage", "year", "gearbox", "transmission", "horsepower", "energie", "location", "price", "date"])

# Fonction pour scraper une page
def scrape_page(page_num):
    url = BASE_URL.format(page_num)
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Erreur {response.status_code} lors de l'accès à {url}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all('div', {'class': 'thumb-caption'})

    for result in results:
        try:
            # Extraire la date et vérifier si elle est dans la période cible
            date_str = result.find('div', class_='date-posted')
            date_str = date_str.get_text(strip=True) if date_str else 'n/a'

            if date_str != 'n/a':
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    if not (datetime(2025, 1, 1) <= date_obj <= datetime(2025, 2, 28)):
                        continue  # On ignore les annonces hors période
                except ValueError:
                    print(f"Format de date invalide : {date_str}")
                    continue
            
            # Scraping des informations
            Name.append(result.find('h2').get_text(strip=True) if result.find('h2') else 'n/a')
            Mileage.append(result.find('li', {'class': 'road'}).get_text(strip=True) if result.find('li', {'class': 'road'}) else 'n/a')
            Year.append(result.find('li', {'class': 'year'}).get_text(strip=True) if result.find('li', {'class': 'year'}) else 'n/a')
            Gearbox.append(result.find('li', {'class': 'boite'}).get_text(strip=True) if result.find('li', {'class': 'boite'}) else 'n/a')
            Transmission.append(result.find('li', {'class': 'transmission'}).get_text(strip=True) if result.find('li', {'class': 'transmission'}) else 'n/a')
            Horse_Power.append(result.find('li', {'class': 'horsepower'}).get_text(strip=True) if result.find('li', {'class': 'horsepower'}) else 'n/a')
            Energie.append(result.find('li', {'class': 'fuel'}).get_text(strip=True) if result.find('li', {'class': 'fuel'}) else 'n/a')

            location_span = result.find('span', class_='fw-medium text-muted d-inline-flex align-items-center')
            Location.append(location_span.get_text(strip=True).replace('\xa0', ' ') if location_span else 'n/a')

            price_div = result.find('div', class_='price')
            Price.append(price_div.get_text(strip=True).replace('\xa0', ' ') if price_div else 'n/a')



            Dates.append(date_str)

        except Exception as e:
            print(f"Erreur avec une annonce : {e}")

# Boucle sur plusieurs pages (1 à 10)
for i in range(1, 11):
    print(f"Scraping de la page {i}...")
    scrape_page(i)

# Création du DataFrame
car_dealer = pd.DataFrame({
    'Name': Name, 'Mileage': Mileage, 'Year': Year, 'Gearbox': Gearbox,
    'Transmission': Transmission, 'Horse Power': Horse_Power, 'Energie': Energie,
    'Location': Location, 'Price': Price, 'Date': Dates
})


# Affichage des 5 premières annonces stockées
df = fetch_annonces()
print(df.head())


# Sauvegarde en CSV
car_dealer.to_csv('car_dealer_filtered.csv', index=False, encoding='utf-8')
print("Scraping terminé et fichier enregistré ")





