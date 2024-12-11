# from dash import html, register_page, dcc, html, callback, Input, Output
# # from dash import html, dcc  # Ensure correct imports for Dash components

# register_page(__name__, path="/plays")
# layout = html.Div([
    
#     html.H1("in here display simulation of games compared!"),
# #     html.Div(
# #     className="card",
# #     children=[
# #         html.H4("Team Name", style={"margin-bottom": "15px"}),
# #         html.P("This is a simple card example in Dash."),
# #     ]
# # ),
#         html.Div([
#         dcc.Link("Back to Home", href="/")
#     ])
#     # html.P("Use the navigation bar to go to the comparison page.")
# ])
# # show charts of game.
# # show charts of play by play (play1, play2,.. etc)
# @callback(
#     Output('game-details', 'children'),
#     Input('url', 'pathname')
# )
# def display_game_details(pathname):
#     # Extract game_id from URL path
#     game_id = pathname.split('/')[-1]  # Get the part after '/plays/'
    
#     # Here, you'd query your data for the specific game details based on the game_id
#     # For now, we'll just display the game ID for testing
#     return html.Div(f"Details for {game_id}: This is where game-specific analysis would go.")

# simulationResults.py
from dash import html, register_page, callback, Input, Output, dcc

# Register dynamic page with game_id parameter
register_page(__name__, path="/plays/game_id")

layout = html.Div([
    html.H1("Display Simulation of Games Compared"),
    html.Div(id='game-details'),  # This will hold the specific game details
    dcc.Link("Back to Home", href="/")
])

@callback(
    Output('game-details', 'children'),
    Input('url', 'pathname')  # Capture the URL path to extract the game ID
)
def display_game_details(pathname):
    # Extract game_id from the URL path (last part after '/plays/')
    game_id = pathname.split('/')[-1]  # The game_id is the last segment of the URL path
    
    # You can replace this with actual data or queries for game analysis
    return html.Div(f"Details for Game ID: {game_id}")


