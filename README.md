scraping-voitures-tunisie/
├── scraper.py           # Script de scraping des annonces
├── app.py               # Tableau de bord interactif Dash
├── car_dealer_filtered.csv # Données exportées du scraping
├── annonces.db          # Base de données SQLite
├── requirements.txt     # Dépendances du projet
├── test_db.py           # Test de la base de données
└── README.md            # Ce fichier

 Installation et Lancement
1. Cloner le projet
git clone https://github.com/hmaidinour/scraping-voitures-tunisie.git
cd scraping-voitures-tunisie

2. Installer les dépendances
pip install -r requirements.txt

3. Lancer le scraper (Partie 1)
python scraper.py
Les données seront stockées dans annonces.db et car_dealer_filtered.csv.

4. Lancer le tableau de bord (Partie 2)
python app.py
Accédez au tableau de bord dans votre navigateur :
http://127.0.0.1:8050/
