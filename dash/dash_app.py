import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import requests
from io import BytesIO

# Initialize the Dash app with Bootstrap for styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = dbc.Container(
    [
        html.H1("Assets Management", className="text-center mt-3"),
        # Section: Form for Creating/Updating Assets
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Add or Update Asset"),
                        dbc.Form(
                            [
                                dbc.Input(
                                    id="asset-name",
                                    placeholder="Name",
                                    type="text",
                                    className="mb-2",
                                ),
                                dbc.Input(
                                    id="asset-barcode",
                                    placeholder="Barcode",
                                    type="text",
                                    className="mb-2",
                                ),
                                dbc.Input(
                                    id="asset-barcode-type",
                                    placeholder="Barcode Type",
                                    type="text",
                                    className="mb-2",
                                ),
                                dbc.Input(
                                    id="asset-type",
                                    placeholder="Asset Type",
                                    type="text",
                                    className="mb-2",
                                ),
                                dbc.Textarea(
                                    id="asset-description",
                                    placeholder="Description",
                                    className="mb-2",
                                ),
                                dbc.Button(
                                    "Submit",
                                    id="submit-button",
                                    color="primary",
                                    className="mt-2",
                                ),
                            ]
                        ),
                    ],
                    width=4,
                ),
                # Section: Display and Export
                dbc.Col(
                    [
                        html.H3("Assets List"),
                        dcc.Loading(
                            id="loading-table",
                            type="default",
                            children=html.Div(id="table-container"),
                        ),
                        dbc.Button(
                            "Export to Excel",
                            id="export-button",
                            color="secondary",
                            className="mt-3",
                        ),
                        dcc.Download(id="download-excel"),
                    ],
                    width=4,
                ),
                # Section: Bulk create update
                dbc.Col(
                    [
                        html.H3("Assets List"),
                        dcc.Loading(
                            id="loading-table",
                            type="default",
                            children=html.Div(id="table-container"),
                        ),
                        dbc.Button(
                            "upload",
                            id="export-button",
                            color="secondary",
                            className="mt-3",
                        ),
                        dcc.Download(id="download-excel"),
                    ],
                    width=4,
                ),
            ]
        ),
    ],
    fluid=True,
)


# Define API URL
API_URL = "http://10.1.200.42:5000"  # API root url


# Callback to submit (create or update) an asset
@app.callback(
    Output("table-container", "children"),
    Input("submit-button", "n_clicks"),
    [
        State("asset-name", "value"),
        State("asset-barcode", "value"),
        State("asset-barcode-type", "value"),
        State("asset-type", "value"),
        State("asset-description", "value"),
    ],
)
def submit_asset(n_clicks, name, barcode, barcode_type, asset_type, description):
    if not n_clicks:
        return ""

    # Prepare data
    asset_data = {
        "name": name,
        "barcode": barcode,
        "barcode_type": barcode_type,
        "asset_type": asset_type,
        "description": description,
    }

    # Send request to Flask API
    response = requests.post(API_URL, json=asset_data)

    # Fetch and display the updated list of assets
    return update_table()


# Function to update the table with paginated assets
def update_table():
    response = requests.get(f"{API_URL}/records")
    assets = response.json() if response.status_code == 200 else []

    # Convert to DataFrame for easy manipulation
    df = pd.DataFrame(assets)

    # Render table in Dash
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)


# Callback to export assets to Excel
@app.callback(
    Output("download-excel", "data"),
    Input("export-button", "n_clicks"),
    prevent_initial_call=True,
)
def export_to_excel(n_clicks):
    response = requests.get(f"{API_URL}/export", stream=True)

    if response.status_code == 200:
        return dcc.send_bytes(response.content, filename="exported_data.xlsx")
    else:
        return None


if __name__ == "__main__":
    app.run_server(debug=True)
