import time
from tkinter import ALL
from dash import html, register_page
from dash import html, dcc,Output, Input, State, callback  # Ensure correct imports for Dash components
import dash
import nfl_data_py as nfl
import pandas as pd
# to see output of gameLoop.py
import gameLoop as gameSimulation
# # gameData = nfl.import_seasonal_data([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010], 'ALL')
# # gameDataFrame = pd.DataFrame(gameData)
# import plotly.graph_objects as go
# # x = gameDataFrame['season']  # Replace with the actual column name for the x-axis
# # y = gameDataFrame['completions']  # Replace with the actual column name for the y-axis
# # line_plot = go.Figure(
# #     data=[go.Scatter(x=x, y=y, mode='lines+markers', name='Points Scored')],
# #     layout=go.Layout(
# #         title='Points Scored Over Games',
# #         xaxis=dict(title='Game Number'),
# #         yaxis=dict(title='Points Scored'),
# #         template='plotly_dark'
# #     )
# # )
# register_page(__name__, path="/games")
# layout = html.Div([
#     dcc.Store(id='input-data-store', storage_type='session'),
#     html.Div(
#         id="loading-animation",
#         className="box",
#         children=[
#             html.Div(className="shadow"),
#             html.Div(className="gravity", children=[
#                 html.Div(className="ball")
#             ])
#         ],
#         style={"display": "block"}
#     ),
#     html.Div(
#         id="content-container",
#         style={"display": "none"},
#         children=[
#             html.H1("List of Games Compared"),
#             # dcc.Graph(figure=line_plot),
#             html.Div(id='games-output', className='games-list'),  # Placeholder for game cards
#             html.Div(id='selected-game-output', className='game-details') ,
#             html.Button("Download CSV", id="download-btn"),
#             # Download component
#             dcc.Download(id="download-df-csv") # Placeholder for game details
#         ]
#     )
# ])

# # layout = html.Div([
# #     dcc.Store(id='input-data-store', storage_type='session'),  # Ensure compatibility
# #     html.Div(
# #         id="loading-animation",
# #         className="box",
# #         children=[
# #             html.Div(className="shadow"),
# #             html.Div(className="gravity", children=[
# #                 html.Div(className="ball")  # Ball animation which is shown for lading
# #             ])
# #         ],
# #         style={"display": "block"}  # Initially visible
# #     ),
# #     # My content container which will be hidden until data loads
# #     html.Div(
# #         id="content-container",
# #         style={"display": "none"},  # Initially hidden
# #         children=[
# #             html.H1("List of Games Compared"),
# #             dcc.Graph(figure=line_plot),
# #             html.Div(
# #                 dcc.Link(
# #                     href="/plays",
# #                     className="card",
# #                     children=[
# #                         html.H4("Team Name", style={"margin-bottom": "15px"}),
# #                         html.P("This is a simple card example in Dash."),
# #                     ]
# #                 )
# #             ),
# #             html.Div(id='games-output'),
# #             html.Div([
# #                 # dcc.Link("Plays", href="/plays"),
# #                 dcc.Link("Back to Home", href="/")
# #             ]),
# #             # Button to download the CSV
# #             html.Button("Download CSV", id="download-btn"),
# #             # Download component
# #             dcc.Download(id="download-df-csv")
# #         ]
# #     )
# # ])
# # Callback to simulate data loading and toggle visibility
# @callback(
#     [Output("loading-animation", "style"), Output("content-container", "style")],
#     [Input("loading-animation", "id")],  # Trigger on page load
#     prevent_initial_call=False  # Allow triggering on initial page load
# )
# def simulate_loading(_):
#     """Simulate a loading delay"""
#     time.sleep(20)  # Simulates content loading delay
#     # Toggle visibility: Hide animation, show content
#     return {"display": "none"}, {"display": "block"}
# @callback(
#     Output('games-output', 'children'),
#     Input('input-data-store', 'data')  # Access stored data
# )

# def display_game_results(data):
#     global total_games_dataFrame
#     if not data:
#         return "No data provided. Please return to the dashboard to input your selections."

#     total_games_data = getTotalGames(data)
#     all_games_data = [pd.DataFrame(game) for game in total_games_data]
#     total_games_dataFrame = pd.concat(all_games_data, ignore_index=True)

#     # Create dynamic cards with unique `id` using a dict
#     results = [
#         html.Div(
#             f"Game {i + 1}",
#             className='card',
#             id={'type': 'game-card', 'index': i}  # Assign unique ID as dict
#         )
#         for i in range(len(all_games_data))
#     ]
#     return results
# @callback(
#     Output('selected-game-output', 'children'),
#     Input({'type': 'game-card', 'index': ALL}, 'n_clicks'),
#     prevent_initial_call=True
# )
# def show_game_details(n_clicks_list):
#     # Check which card was clicked
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return "Click on a game to view details."

#     # Find the index of the clicked game card
#     clicked_card_index = [
#         idx for idx, n_clicks in enumerate(n_clicks_list) if n_clicks
#     ]
#     if not clicked_card_index:
#         return "No game selected."
#     selected_game_index = clicked_card_index[0]

#     # Extract data for the selected game
#     selected_game_df = total_games_dataFrame.iloc[selected_game_index]

#     # Return details as a DataTable
#     return dash.dash_table.DataTable(
#         data=selected_game_df.to_dict('records'),
#         columns=[{"name": col, "id": col} for col in selected_game_df.index],
#         style_table={'overflowX': 'auto'},
#         style_cell={'textAlign': 'left', 'padding': '5px'},
#         style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
#         style_data={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
#     )


# def getTotalGames(data):
#     totalGames = gameSimulation.runSimulation(homeTeam=data['homeTeam'],awayTeam=data['awayTeam'],numGames=int(data['num_games']))[0]
#     return totalGames
# # CSV DOWNLOAD FUNCTIONALITY

# # Callback for the download functionality
# @callback(
#     Output("download-df-csv", "data"),
#     Input("download-btn", "n_clicks"),
#     prevent_initial_call=True
# )
# def export_csv(n_clicks):
#     """Exports the DataFrame as a CSV when the button is clicked."""
#     # for each game in df 
#     for game in total_games_dataFrame:
#         frameData=[pd.DataFrame(game)]
#         combined_data=pd.concat(frameData,ignore_index=False)
#         csv_string = combined_data.to_csv(index=True)
#     # Return the CSV file for download
#     return dcc.send_string(csv_string, filename="GameData.csv")
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
        #  html.Div([
        #     dcc.Tabs(id="tabs",value="",children=[(dcc.Tab(a)) for a in [1,2,3]]),
        #     html.Div(id='tabs-content')
        #     ]),
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
def simulate_loading(_):
    time.sleep(20)  # Simulated content loading delay
    return {"display": "none"}, {"display": "block"}

# Display game results (cards)
@callback(
    Output('games-output', 'children'),
    Input('input-data-store', 'data')  # Access stored data
)
# def display_game_results(data):
#     global total_games_data
#     if not data:
#         return "No data provided. Please return to the dashboard to input your selections."
#     total_games_data = getTotalGames(data)
#     print("length of total_games_data:",len(total_games_data),"what is in it: ",total_games_data)
#     results = [
#             #     html.Div([
#             # dcc.Tabs(id="tabs",value="",children=[(dcc.Tab(a)) for a in total_games_data]),
#             # html.Div(id='tabs-content')
#             # ]),
#         html.Div(
#             f"Game {i + 1}",
#             className='card',
#             id={'type': 'game-card', 'index': i}  # Assign unique ID as dict
#         )
#         for i in range(len(total_games_data))
#     ]
    
#     return results

# @callback(
#     Output('selected-game-output', 'children'),
#     Input({'type': 'game-card', 'index': ALL}, 'n_clicks'),
#     prevent_initial_call=True
# )
# def show_game_details(n_clicks_list):
#      print(n_clicks_list)
#      clicked_card_index = [
#         idx for idx, n_clicks in enumerate(n_clicks_list) if n_clicks
#     ]
#      print(clicked_card_index)
#     # for game in total_games_data:
#     #     print(f"game: ",game)
        
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
    print("clicked button",n_clicks_list)
    ctx = dash.callback_context
    if not ctx.triggered:
        return "Click on a game to view details."
    # clicked_card_index = [
    #     idx for idx, n_clicks in enumerate(n_clicks_list) if n_clicks
    # ]
    # if not clicked_card_index:
    #     return "No game selected."
    # selected_game_index = clicked_card_index[-1]
    # Find the index of the last clicked game card
    # valid_clicks = [
    #     (idx, clicks) for idx, clicks in enumerate(n_clicks_list) if clicks
    # ]

    # if not valid_clicks:
    #     return "No game selected."

    # # Extract the index of the last clicked card
    # clicked_card_index = max(valid_clicks, key=lambda x: x[1])[0]
    # print(f"Selected card index: {clicked_card_index}")
    
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
    return dash.dash_table.DataTable(
        data=selected_game_df.to_dict('records'),
        columns=[{"name": col, "id": col} for col in selected_game_df],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px'},
        style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
        style_data={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
    )


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
    global total_games_dataFrame
    """Exports the DataFrame as a CSV when the button is clicked."""
    if total_games_dataFrame.empty:
        return "No data available to download"
    
    csv_string = total_games_dataFrame.to_csv(index=True)
    return dcc.send_string(csv_string, filename="GameData.csv")