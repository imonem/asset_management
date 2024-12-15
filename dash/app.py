import dash
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, callback, html
from flask import Flask
from utils.api import API

import pandas as pd
import requests

from components.navbar import navbar

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

server = Flask(__name__)
app = Dash(
    __name__,
    server=server,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="GS1 Egypt Asset Management App ",
    external_stylesheets=[
        dbc.themes.SPACELAB,
        dbc_css,
        dbc.icons.FONT_AWESOME,
    ],  # Added dbc_css to style Dash DataTable Component
)


content = html.Div(
    [
        dash.page_container,
    ]
)


def serve_app_layout():
    return dbc.Container(
        children=[
            navbar,
            content,
        ]
    )


app.layout = (
    serve_app_layout  # https://dash.plotly.com/live-updates#updates-on-page-load
)


# add callback for toggling the collapse on small screens
@callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# # Function to update the table with paginated assets
def update_table():
    response = requests.get(f"{API}/records")
    assets = response.json() if response.status_code == 200 else []

    # Convert to DataFrame for easy manipulation
    df = pd.DataFrame(assets)

    # Render table in Dash
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)


if __name__ == "__main__":
    app.run(debug=True)
