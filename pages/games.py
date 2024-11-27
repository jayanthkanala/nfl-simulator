from dash import html, register_page
from dash import html, dcc  # Ensure correct imports for Dash components

register_page(__name__, path="/games")

layout = html.Div([
    html.H1("in here display all list of games compared!"),
    html.Div(
        dcc.Link(
        href="/plays",
    className="card",
    children=[
        html.H4("Team Name", style={"margin-bottom": "15px"}),
        html.P("This is a simple card example in Dash."),
    ]
    )),
    # routing to page
            html.Div([
        dcc.Link("Plays", href="/plays")
    ]),
        html.Div([
        dcc.Link("Back to Home", href="/")
    ])
    # html.P("Use the navigation bar to go to the comparison page.")
    
])
# show a chart
# then loop list and show in cards(games)
# click on the game to access stats of game (play by play).
