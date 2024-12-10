import time
from tkinter import ALL
from dash import html, register_page
from dash import html, dcc,Output, Input, State, callback  # Ensure correct imports for Dash components
import dash
import nfl_data_py as nfl
import pandas as pd
# to see output of gameLoop.py
import gameLoop as gameSimulation
import time
from dash import html, dcc, Output, Input, callback, ALL
import dash
import pandas as pd
import nfl_data_py as nfl
import gameLoop as gameSimulation

# Initialize Dash app
app = dash.Dash(__name__)
register_page(__name__, path="/games")

# # Global variable to store total games data
# total_games_dataFrame = pd.DataFrame()

# Layout
layout = html.Div([
    dcc.Store(id='input-data-store', storage_type='session'),  # Store input data temporarily
    html.Div(
        id="loading-animation",
        className="box",
        children=[
            html.Div(className="shadow"),
            html.Div(className="gravity", children=[html.Div(className="ball")])
        ],
        style={"display": "block"}
    ),
    html.Div(
        id="content-container",
        style={"display": "none"},
        children=[
html.Div(
    children=[
        html.H1("Play by Play Simulation Results"),
        html.Div(
            children=[
                html.Div(id='games-output', className='games-list'),  # Placeholder for game cards
                html.Div(id='selected-game-output', className='game-details')  # Placeholder for game details
            ],
            style={
                "display": "flex",  # Enables flexbox
                "gap": "20px",  # Adds spacing between the two divs
                "alignItems": "flex-start"  # Aligns items to the top
            }
        ),
        html.Button("Download CSV", id="download-btn"),
        dcc.Download(id="download-df-csv")
    ]
)
        ]
    )
])

# Simulate data loading (20s delay for simulation)
@callback(
    [Output("loading-animation", "style"), Output("content-container", "style")],
    [Input("loading-animation", "id")],  # Trigger on page load
    prevent_initial_call=False
)
def simulate_loading(flag):
    time.sleep(20)  # Simulated content loading delay
    return {"display": "none"}, {"display": "block"}

# Display game results (cards)
@callback(
    Output('games-output', 'children'),
    Input('input-data-store', 'data')  # Access stored data
)
        
def display_game_results(data):
    global all_games_data
    if not data:
        return "No data provided. Please return to the dashboard to input your selections."

    total_games_data = getTotalGames(data)
    all_games_data = [pd.DataFrame(game) for game in total_games_data]
    # total_games_dataFrame = pd.concat(all_games_data, ignore_index=True)

    # Create dynamic cards with unique `id` using a dict
    results = [
        html.Div(
            f"Game {i + 1}",
            className='card',
            id={'type': 'game-card', 'index': i}  # Assign unique ID as dict
        )
        for i in range(len(total_games_data))
    ]
    return results

# Show details of selected game
@callback(
    Output('selected-game-output', 'children'),
    Input({'type': 'game-card', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def show_game_details(n_clicks_list):
    global clicked_card_index
    print("clicked button",n_clicks_list)
    ctx = dash.callback_context
    if not ctx.triggered:
        return "Click on a game to view details."
    
    # Debugging: Log the triggered context
    print("Callback context triggered:", ctx.triggered)

    # Extract the ID of the triggered component
    triggered_id = ctx.triggered[0]['prop_id']

    # Use regex or directly parse the ID to find the `index`
    try:
        # For `ALL`, the ID is typically a dictionary like {'type': 'game-card', 'index': X}
        # Extract the `index` from the ID
        triggered_id_dict = eval(triggered_id.split(".")[0])
        clicked_card_index = triggered_id_dict["index"]
    except (KeyError, SyntaxError) as e:
        print(f"Error extracting index from triggered ID: {triggered_id}")
        return "Error: Unable to determine the clicked game."

    print(f"Selected card index: {clicked_card_index}")

    # Extract data for the selected game
    selected_game_df = all_games_data[clicked_card_index] #convering to df because it forms a series
    # selected_game_df =total_games_data[clicked_card_index]
    print("selected_game_df: ",selected_game_df)
    # Return details as a DataTable
    return html.Div([
        html.Label(f"Game-{clicked_card_index + 1}", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': 'red'}),
        dash.dash_table.DataTable(
        data=selected_game_df.to_dict('records'),
        columns=[{"name": col, "id": col} for col in selected_game_df],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px'},
        style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
        style_data={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
    )
    ])


# Function to run simulations and return total game data
def getTotalGames(data):
    totalGames = gameSimulation.runSimulation(homeTeam=data['homeTeam'], awayTeam=data['awayTeam'], numGames=int(data['num_games']))[0]
    return totalGames

# Callback for the download functionality
@callback(
    Output("download-df-csv", "data"),
    Input("download-btn", "n_clicks"),
    prevent_initial_call=True
)
def export_csv(n_clicks):
    """Exports the DataFrame as a CSV when the button is clicked."""
    if not all_games_data:
        return "No data available to download"

    # Convert to CSV string
    csv_string = all_games_data[clicked_card_index].to_csv(index=True)
    # for game in all_games_data[clicked_card_index]:
    #     csv_string=game.to_csv(index=True)

    # Send the CSV as a downloadable file
    return dcc.send_string(csv_string, filename=f"GameData_{clicked_card_index}.csv")
