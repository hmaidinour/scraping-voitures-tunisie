import sqlite3

# Connexion à la base SQLite
conn = sqlite3.connect("annonces.db")
cursor = conn.cursor()

# Vérifier si des données sont présentes dans la table "annonces"
cursor.execute("SELECT * FROM annonces LIMIT 5;")  # Afficher 5 premières lignes
rows = cursor.fetchall()

# Affichage des résultats
if rows:
    for row in rows:
        print(row)
else:
    print("Aucune donnée trouvée dans la base")

# Fermer la connexion
conn.close()
