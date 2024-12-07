import time
from dash import html, register_page
from dash import html, dcc,Output, Input, State, callback  # Ensure correct imports for Dash components
import nfl_data_py as nfl
import pandas as pd
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
                dcc.Link("Plays", href="/plays"),
                dcc.Link("Back to Home", href="/")
            ]),
            # Button to download the CSV
            html.Button("Download CSV", id="download-btn"),
            # Download component
            dcc.Download(id="download-df-csv"),
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