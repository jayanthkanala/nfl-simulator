import time
from dash import html, register_page
from dash import html, dcc,Output, Input, State, callback  # Ensure correct imports for Dash components
import nfl_data_py as nfl
import pandas as pd
# to see output of gameLoop.py
from gameLoop import main
res = main()
print(res)
gameData = nfl.import_seasonal_data([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010], 'ALL')
gameDataFrame = pd.DataFrame(gameData)
import plotly.graph_objects as go
x = gameDataFrame['season']  # Replace with the actual column name for the x-axis
y = gameDataFrame['completions']  # Replace with the actual column name for the y-axis
line_plot = go.Figure(
    data=[go.Scatter(x=x, y=y, mode='lines+markers', name='Points Scored')],
    layout=go.Layout(
        title='Points Scored Over Games',
        xaxis=dict(title='Game Number'),
        yaxis=dict(title='Points Scored'),
        template='plotly_dark'
    )
)
register_page(__name__, path="/games")
layout = html.Div([
    dcc.Store(id='input-data-store', storage_type='session'),  # Ensure compatibility
    html.Div(
        id="loading-animation",
        className="box",
        children=[
            html.Div(className="shadow"),
            html.Div(className="gravity", children=[
                html.Div(className="ball")  # Ball animation which is shown for lading
            ])
        ],
        style={"display": "block"}  # Initially visible
    ),
    # My content container which will be hidden until data loads
    html.Div(
        id="content-container",
        style={"display": "none"},  # Initially hidden
        children=[
            html.H1("List of Games Compared"),
            dcc.Graph(figure=line_plot),
            html.Div(
                dcc.Link(
                    href="/plays",
                    className="card",
                    children=[
                        html.H4("Team Name", style={"margin-bottom": "15px"}),
                        html.P("This is a simple card example in Dash."),
                    ]
                )
            ),
            html.Div([
                # dcc.Link("Plays", href="/plays"),
                dcc.Link("Back to Home", href="/")
            ]),
            # Button to download the CSV
            html.Button("Download CSV", id="download-btn"),
            # Download component
            dcc.Download(id="download-df-csv"),
             html.Div(id='games-output')
        ]
    )
])
# Callback to simulate data loading and toggle visibility
@callback(
    [Output("loading-animation", "style"), Output("content-container", "style")],
    [Input("loading-animation", "id")],  # Trigger on page load
    prevent_initial_call=False  # Allow triggering on initial page load
)
def simulate_loading(_):
    """Simulate a loading delay"""
    time.sleep(3)  # Simulates content loading delay
    # Toggle visibility: Hide animation, show content
    return {"display": "none"}, {"display": "block"}
@callback(
    Output('games-output', 'children'),
    Input('input-data-store', 'data')  # Access stored data
)

def display_game_results(data):
    if not data:
        return "No data provided. Please return to the dashboard to input your selections."
    
    # # Extract stored values
    # home_team = data.get('home_team', 'N/A')
    # away_team = data.get('away_team', 'N/A')
    # year = data.get('year', 'N/A')
    # weather = data.get('weather', 'N/A')
    # num_games = data.get('num_games', 'N/A')
    # team_a_loc = data.get('team_a_loc', 'N/A')
    # team_b_loc = data.get('team_b_loc', 'N/A')
    # game_ids = [f"game_{i+1}" for i in range(20)]
    results = [
        html.Div(
            children=[
                dcc.Link(
                    html.Div(f"Game {i+1}: Placeholder for game analysis.", className='card'),
                    href=f'/plays/{data['num_games']}',  # Pass the specific game ID in the URL
                    className='game-link'
                )
            ],
            className='game-result-container'
        )
        for i in range(int(data['num_games']))
    ]
    
    # Render the inputs dynamically
    return results

# CSV DOWNLOAD FUNCTIONALITY

# Callback for the download functionality
@callback(
    Output("download-df-csv", "data"),
    Input("download-btn", "n_clicks"),
    prevent_initial_call=True
)
def export_csv(n_clicks):
    """Exports the DataFrame as a CSV when the button is clicked."""
    csv_string = gameDataFrame.to_csv(index=False)
    # Return the CSV file for download
    return dcc.send_string(csv_string, filename="GameData.csv")