from dash import html, register_page
from dash import html, dcc  # Ensure correct imports for Dash components
import nfl_data_py as nfl
gameData = nfl.import_seasonal_data([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010], 'ALL')
print(gameData)
import plotly.graph_objects as go
x = gameData['season']  # Replace with the actual column name for the x-axis
y = gameData['completions']  # Replace with the actual column name for the y-axis
# # Create a line chart
# line_chart = go.Figure(
#     data=[go.Scatter(x=x, y=y, mode='lines', name='Game Data Rosters')],
#     layout=go.Layout(
#         title='Game Data: Points Scored Over Games',
#         xaxis=dict(title='season'),
#         yaxis=dict(title='completions')
#     )
# )
#  a line plot using go.Scatter
line_plot = go.Figure(
    data=[go.Scatter(x=x, y=y, mode='lines+markers', name='Points Scored')],
    layout=go.Layout(
        title='Points Scored Over Games',
        xaxis=dict(title='Game Number'),
        yaxis=dict(title='Points Scored'),
        template='plotly_dark'  # Optional: set dark theme, can be customized
    )
)
register_page(__name__, path="/games")

layout = html.Div([
    html.H1("in here display all list of games compared!"),
    # dcc.Graph(figure=line_chart),
    dcc.Graph(figure=line_plot),
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
