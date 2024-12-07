import datetime
from dash import html, dcc, register_page, Output, Input, State, callback
import dash
import dash_bootstrap_components as dbc
import nfl_data_py as nfl

# Register the page with the path "/dashboard"
register_page(__name__, path="/")

# Fetch data for dropdowns
weather_conditions = ['Sunny', 'Rainy', 'Snowy', 'Cloudy']
teams = nfl.import_team_desc()['team_name'].tolist()
logos= nfl.import_team_desc()['team_logo_squared'].tolist()
current_year = datetime.datetime.now().year
year_range = range(1999, current_year + 1)

# Page layout
layout = html.Div([
    dcc.Store(id='input-data-store', storage_type='session'),  # Store component to hold user inputs
    dcc.Location(id='url', refresh=True),  # Component for URL redirection
    html.H2("NFL Team Comparison Dashboard"),
    
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
      # Logos for selected teams
    html.Div(id='logos-container', className='logo-container'),

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
        html.Button('Compare', id='submit-button', n_clicks=0),
    ], className='dropdown-container submit-button'),

    # Output Section
    html.Div(id='output', className='output-container'),
    html.Div([
        dcc.Link("Games", href="/games")
    ])
])

# Callback for input validation and output generation
@callback(
    [Output('input-data-store', 'data'),  # Save user inputs in the store
     Output('output', 'children'),       # For validation messages
     Output('url', 'pathname')],         # Redirect to the "/games" page
    Input('submit-button', 'n_clicks'),
    State('home_team', 'value'),
    State('away_team', 'value'),
    State('year', 'value'),
    State('weather', 'value'),
    State('num-games', 'value'),
    State('team-a-loc', 'value'),
    State('team-b-loc', 'value'),
)
def save_inputs_and_redirect(n_clicks, home_team, away_team, year, weather, num_games, team_a_loc, team_b_loc):
    if n_clicks > 0:
        # Validation
        if not home_team or not away_team:
            return {}, "Please select both Home Team and Away Team .", dash.no_update
        if not team_a_loc or not team_b_loc:
            return {}, "Please select locations for both Home Team and Away Team .", dash.no_update
        if not year:
            return {}, "Please select a year.", dash.no_update
        if not weather:
            return {}, "Please select weather conditions.", dash.no_update
        if not num_games or int(num_games) <= 0:
            return {}, "Please enter a valid number of games (1-10).", dash.no_update
        
        # Save inputs to the store
        data = {
            'home_team': home_team,
            'away_team': away_team,
            'year': year,
            'weather': weather,
            'num_games': num_games,
            'team_a_loc': team_a_loc,
            'team_b_loc': team_b_loc,
        }
        print("data in dashboard:",data)
        return data, "Inputs saved successfully.", "/games"  # Redirect to /games

    return {}, "", dash.no_update  # Default response
@callback(
    Output('logos-container', 'children'),
    [Input('home_team', 'value'), Input('away_team', 'value')]
)
# TO FETCH SELECTED TEAMS LOGOS:
def update_logos(home_team, away_team):
    """
    Conditionally renders the logos for the selected teams and adds 'Vs' between them.

    Args:
        home_team (str): Selected team A.
        away_team (str): Selected team B.

    Returns:
        list: Children elements containing the logos for the selected teams and "Vs" text."""
    children = []

    # Add Team A's logo if selected
    if home_team:
        team_a_index = teams.index(home_team) if home_team in teams else None
        team_a_logo = logos[team_a_index] if team_a_index is not None else ""
        if team_a_logo:
            children.append(html.Img(src=team_a_logo, height='100px', style={'margin-right': '10px'}))

    # Add 'Vs' text between logos if both teams are selected
    if home_team and away_team:
        children.append(html.Div(" Vs ", style={'font-size': '24px', 'margin': '0 10px', 'font-weight': 'bold'}))

    # Add Team B's logo if selected
    if away_team:
        team_b_index = teams.index(away_team) if away_team in teams else None
        team_b_logo = logos[team_b_index] if team_b_index is not None else ""
        if team_b_logo:
            children.append(html.Img(src=team_b_logo, height='100px'))

    # Return the children to display the logos with "Vs" in between
    return children