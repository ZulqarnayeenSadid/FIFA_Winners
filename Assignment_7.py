
#Loading the required libraries
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output

#Create DataSet

# Dataset for FIFA World Cup winners and runners-up
data = {
    "Year": [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022],
    "Winners": ["Uruguay", "Italy", "Italy", "Uruguay", "West Germany", "Brazil", "Brazil", "England", "Brazil", "West Germany", "Argentina", "Italy", "Argentina", "West Germany", "Brazil", "France", "Brazil", "Italy", "Spain", "Germany", "France", "Argentina"],
    "Runners-up": ["Argentina", "Czechoslovakia", "Hungary", "Brazil", "Hungary", "Sweden", "Czechoslovakia", "West Germany", "Italy", "Netherlands", "Netherlands", "West Germany", "West Germany", "Argentina", "Italy", "Brazil", "Germany", "France", "Netherlands", "Argentina", "Croatia", "France"]
}

# Create DataFrame
fifa_data = pd.DataFrame(data)

# Replace West Germany with Germany for consistency
fifa_data['Winners'] = fifa_data['Winners'].replace('West Germany', 'Germany')
fifa_data['Runners-up'] = fifa_data['Runners-up'].replace('West Germany', 'Germany')

# Calculate the number of wins for each country
wins_count = fifa_data['Winners'].value_counts().reset_index()
wins_count.columns = ['country', 'wins']

# Create choropleth map
fig = px.choropleth(
    wins_count,
    locations="country",
    locationmode="country names",
    color="wins",
    title="FIFA World Cup Winners",
    color_continuous_scale="Viridis"
)

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard"),
    dcc.Graph(figure=fig),
    
    # Dropdown to select a country and view the number of wins
    html.Label("Select a Country:"),
    dcc.Dropdown(
        id="country-dropdown",
        options=[{"label": country, "value": country} for country in fifa_data["Winners"].unique()],
        placeholder="Select a country"
    ),
    html.Div(id="country-wins"),
    
    # Dropdown to select a year and view the winner and runner-up
    html.Label("Select a Year:"),
    dcc.Dropdown(
        id="year-dropdown",
        options=[{"label": year, "value": year} for year in fifa_data["Year"].unique()],
        placeholder="Select a year"
    ),
    html.Div(id="year-result")
])

# Callbacks for dropdown interactions
from dash.dependencies import Input, Output

@app.callback(
    Output("country-wins", "children"),
    Input("country-dropdown", "value")
)
def show_country_wins(selected_country):
    if selected_country:
        wins = wins_count[wins_count['country'] == selected_country]['wins'].values[0]
        return f"{selected_country} has won the World Cup {wins} times."
    return ""

@app.callback(
    Output("year-result", "children"),
    Input("year-dropdown", "value")
)
def show_year_result(selected_year):
    if selected_year:
        winner = fifa_data.loc[fifa_data['Year'] == selected_year, 'Winners'].values[0]
        runner_up = fifa_data.loc[fifa_data['Year'] == selected_year, 'Runners-up'].values[0]
        return f"In {selected_year}, the winner was {winner} and the runner-up was {runner_up}."
    return ""

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
    
