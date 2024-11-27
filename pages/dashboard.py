import datetime
from dash import html, dcc, register_page, Output, Input, State, callback
import dash_bootstrap_components as dbc
import nfl_data_py as nfl

# Register the page with the path "/dashboard"
register_page(__name__, path="/")

# Fetch data for dropdowns
weather_conditions = ['Sunny', 'Rainy', 'Snowy', 'Cloudy']
teams = nfl.import_team_desc()['team_name'].tolist()
current_year = datetime.datetime.now().year
year_range = range(1999, current_year + 1)

# Page layout
layout = html.Div([
    html.H2("Team Comparison Dashboard"),
    
    # Instructions
    html.Div([
        html.P("Select two teams, a year, weather conditions, and the number of games to compare."),
    ], className='instructions'),

    # Team Selection
    html.Div([
        html.Label('Select Team A:', className='label-class'),
        dcc.Dropdown(
            options=[{'label': team, 'value': team} for team in teams],
            value='',  # Default value
            id='home_team',
            className='dropdown-class',
        ),
        html.Label('Select Team B:', className='label-class'),
        dcc.Dropdown(
            options=[{'label': team, 'value': team} for team in teams],
            value='',  # Default value
            id='away_team',
            className='dropdown-class',
        ),
    ], className='dropdown-container'),

    # Location Selection
    html.Div([
        html.Label('Select location for Team A:', className='label-class'),
        dcc.Dropdown(['Home', 'Away'], '', id='team-a-loc', className='dropdown-class'),
        html.Label('Select location for Team B:', className='label-class'),
        dcc.Dropdown(['Home', 'Away'], '', id='team-b-loc', className='dropdown-class')
    ], className='dropdown-container'),

    # Year Selection
    html.Div([
        html.Label('Select Year:', className='label-class'),
        dcc.Dropdown(
            options=[{'label': str(year), 'value': str(year)} for year in year_range],
            value='',  # Default value
            id='year',
            className='dropdown-class',
        ),
    ], className='dropdown-container'),

    # Weather Selection
    html.Div([
        html.Label('Select Weather Conditions:', className='label-class'),
        dcc.Dropdown(
            options=[{'label': condition, 'value': condition} for condition in weather_conditions],
            value='',  # Default value
            id='weather',
            className='dropdown-class',
        ),
    ], className='dropdown-container'),

    # Number of Games
    html.Div([
        html.Label('Select Number of Games:', className='label-class'),
        dcc.Input(id='num-games', type='number', min=1, max=10, placeholder="Enter a number between 1-10", className='input-class')
    ], className='input-container dropdown-container'),

    # Submit Button
    html.Div([
        html.Button('Submit', id='submit-button', n_clicks=0),
    ], className='dropdown-container submit-button'),

    # Output Section
    html.Div(id='output', className='output-container'),
    html.Div([
        dcc.Link("Games", href="/games")
    ])
])

# Callback for input validation and output generation
@callback(
    Output('output', 'children'),
    Input('submit-button', 'n_clicks'),
    State('home_team', 'value'),
    State('away_team', 'value'),
    State('year', 'value'),
    State('weather', 'value'),
    State('num-games', 'value'),
    State('team-a-loc', 'value'),
    State('team-b-loc', 'value'),
)
def update_output(n_clicks, home_team, away_team, year, weather, num_games, team_a_loc, team_b_loc):
    if n_clicks > 0:
        if not home_team or not away_team:
            return "Please select both Team A and Team B."
        if not year:
            return "Please select a year."
        if not weather:
            return "Please select weather conditions."
        if not num_games or int(num_games) <= 0:
            return "Please enter a valid number of games (1-10)."
        
        # If all validations pass
        return (f"Comparison Details:\n"
                f"Team A: {home_team}, Location: {team_a_loc}\n"
                f"Team B: {away_team}, Location: {team_b_loc}\n"
                f"Year: {year}, Weather: {weather}, Games: {num_games}")
    return ""
