# Author: Jayanth Kanala
# Date: Today's date
# Description: Dash application for comparing sports teams with user inputs for team selection, year, weather conditions, and number of games/iterations.

from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    # Title
    html.H1('Team Comparison Dashboard', className='center-cl'),
    
    # Instructions
    html.Div([
        html.P("Select two teams, a year, weather conditions, and the number of games to compare."),
    ], className='instructions'),

    # Team Selection
    html.Div([
        html.Label('Select Team A:', className='label-class'),
        dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'], '', id='team-a', className='dropdown-class'),
        html.Label('Select Team B:', className='label-class'),
        dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'], '', id='team-b', className='dropdown-class')
    ], className='dropdown-container'),

    # Year Selection
    html.Div([
        html.Label('Select Year:', className='label-class'),
        dcc.Dropdown([str(year) for year in range(2000, 2025)], '', id='year', className='dropdown-class')
    ], className='dropdown-container'),

    # Weather Selection
    html.Div([
        html.Label('Select Weather Conditions:', className='label-class'),
        dcc.Dropdown(['Sunny', 'Rainy', 'Snowy', 'Cloudy'], '', id='weather', className='dropdown-class')
    ], className='dropdown-container'),

    # Number of Games
    html.Div([
        html.Label('Select Number of Games:', className='label-class'),
        dcc.Input(id='num-games', type='number', min=1, max=100, placeholder="Enter number between 1-100", className='input-class')
    ], className='input-container dropdown-container'),

    # Submit Button
    html.Div([
        html.Button('Submit', id='submit-button', n_clicks=0),
    ], className='dropdown-container submit-button'),
    # html.Button('Submit', id='submit-button', n_clicks=0, className='submit-button'),

    # Output Section
    html.Div(id='output', className='output-container')
], className='main-class')

# Callback for validation and output display
@app.callback(
    Output('output', 'children'),
    Input('submit-button', 'n_clicks'),
    State('team-a', 'value'),
    State('team-b', 'value'),
    State('year', 'value'),
    State('weather', 'value'),
    State('num-games', 'value')
)
def update_output(n_clicks, team_a, team_b, year, weather, num_games):
    if n_clicks > 0:
        if not team_a or not team_b:
            return "Please select both Team A and Team B."
        if not year:
            return "Please select a year."
        if not weather:
            return "Please select weather conditions."
        if not num_games or num_games <= 0:
            return "Please enter a valid number of games (1-100)."
        
        # If all validations pass
        return (f"Comparison Results:\n"
                f"Team A: {team_a}, Team B: {team_b}, Year: {year}, "
                f"Weather: {weather}, Games: {num_games}")
    return ""

if __name__ == '__main__':
    app.run(debug=True)
