from dash import html, register_page
from dash import html, dcc  # Ensure correct imports for Dash components

register_page(__name__, path="/plays")
layout = html.Div([
    
    html.H1("in here display simulation of games compared!"),
#     html.Div(
#     className="card",
#     children=[
#         html.H4("Team Name", style={"margin-bottom": "15px"}),
#         html.P("This is a simple card example in Dash."),
#     ]
# ),
        html.Div([
        dcc.Link("Back to Home", href="/")
    ])
    # html.P("Use the navigation bar to go to the comparison page.")
])
# show charts of game.
# show charts of play by play (play1, play2,.. etc)