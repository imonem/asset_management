from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import requests

# from dash.dependencies import Input, Output
from utils.api import API


export_button = html.Div(
    id="download-excel",
    children=[
        dbc.Button("Export", external_link=True, href=f"{API}/export"),
        dcc.Download(id="download-dataframe-xlsx"),
    ],
)


# Callback to export assets to Excel
@callback(
    # Output("download-dataframe-xlsx", "data"),
    Input("Export", "n_clicks"),
    prevent_initial_call=False,
    running=[(Output("Export", "disabled"), True, False)],
)
def export_to_excel(n_clicks):
    response = requests.get(f"{API}/export", stream=True)

    if response.status_code == 200:
        return dcc.send_bytes(response.content, filename="exported_data.xlsx")
    else:
        return None
