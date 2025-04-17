import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Charger les données
df = pd.read_csv('car_dealer_filtered.csv')

# Nettoyer les données si besoin
df = df.dropna()

# Créer l'application Dash
app = dash.Dash(__name__)
app.title = "Tableau de Bord - Annonces de Voitures"

# Création des graphiques
fig_energy = px.pie(df, names='Energie', title='Répartition par Énergie')
location_counts = df['Location'].value_counts().reset_index()
location_counts.columns = ['Ville', 'Nombre d\'annonces']

fig_location = px.bar(location_counts, x='Ville', y='Nombre d\'annonces', 
                      labels={'Ville': 'Ville', 'Nombre d\'annonces': 'Nombre d\'annonces'}, 
                      title='Annonces par Ville')
fig_year = px.histogram(df, x='Year', title='Répartition des Annonces par Année')
fig_price = px.histogram(df, x='Price', nbins=20, title='Répartition des Prix des Véhicules')

# Layout de l'application
app.layout = html.Div(children=[
    html.H1("Tableau de Bord - Annonces de Voitures", style={'textAlign': 'center'}),
    
    dcc.Graph(figure=fig_energy),
    dcc.Graph(figure=fig_location),
    dcc.Graph(figure=fig_year),
    dcc.Graph(figure=fig_price),
])

# Lancer le serveur
if __name__ == '__main__':
    app.run(debug=True)

