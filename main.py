from fastapi import FastAPI
from scraper import scrape_page  # Import du scraping
import sqlite3

app = FastAPI()

# Initialiser la base de données SQLite
def init_db():
    conn = sqlite3.connect("annonces.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS annonces (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT, mileage TEXT, year TEXT, gearbox TEXT,
                        transmission TEXT, horsepower TEXT, energie TEXT,
                        location TEXT, price TEXT, date TEXT)''')
    conn.commit()
    conn.close()

init_db()  # Exécuter l'initialisation

# Endpoint pour récupérer les annonces
@app.get("/annonces")
def get_annonces():
    conn = sqlite3.connect("annonces.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM annonces")
    annonces = cursor.fetchall()
    conn.close()
    return {"annonces": annonces}

# Endpoint pour lancer le scraping
@app.post("/scrape")
def start_scraping():
    for i in range(1, 11):  # Scraping sur 10 pages
        scrape_page(i)
    return {"message": "Scraping terminé"}
