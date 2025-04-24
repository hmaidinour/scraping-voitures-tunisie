import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Charger les données
df = pd.read_csv('car_dealer_filtered.csv')

# Nettoyage : convertir les colonnes avec les bons noms (majuscule !)
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Horse Power'] = df['Horse Power'].str.replace(' cv', '', regex=False)
df['Horse Power'] = pd.to_numeric(df['Horse Power'], errors='coerce')

# Supprimer les lignes où Year est manquant
df = df.dropna(subset=['Year'])

# Vérification
print(df.head())

# Créer l'application Dash
app = dash.Dash(__name__)
app.title = "Tableau de Bord - Annonces de Voitures"

# Graphique 1 : Répartition par énergie
fig_energie = px.pie(df, names='Energie', title='Répartition par Énergie')

# Graphique Répartition par Nom (Top 10)
top_names = df['Name'].value_counts().nlargest(10).reset_index()
top_names.columns = ['Nom', 'Nombre d\'annonces']
fig_name = px.bar(top_names, x='Nom', y='Nombre d\'annonces', title='Top 10 des Voitures les plus Annoncées')


# Graphique 3 : Répartition par année
fig_year = px.histogram(df, x='Year', title='Répartition des Annonces par Année')

# Graphique 4 : Répartition par puissance fiscale
fig_hp = px.histogram(df, x='Horse Power', nbins=20, title='Répartition de la Puissance Fiscale')

# Layout Dash
app.layout = html.Div(children=[
    html.H1("Tableau de Bord - Annonces de Voitures", style={'textAlign': 'center'}),
    dcc.Graph(figure=fig_energie),
    dcc.Graph(figure=fig_name),
    dcc.Graph(figure=fig_year),
    dcc.Graph(figure=fig_hp),
])

# Lancer le serveur
if __name__ == '__main__':
    app.run(debug=True)
