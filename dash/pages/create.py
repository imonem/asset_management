import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__, path="/create_one")

layout = html.Div(
    [
        html.H2("Create a New Product"),
        dbc.Form(
            [
                dbc.Input(
                    id="name",
                    placeholder="Product Name",
                    type="text",
                    class_name="mb-2",
                ),
                dbc.Input(
                    id="barcode", placeholder="Barcode", type="text", class_name="mb-2"
                ),
                # Add other fields as needed
                dbc.Button("Create", id="create-button", color="primary"),
            ]
        ),
        html.Div(id="create-output"),
    ]
)

# Callbacks for data creation would go here (e.g., to save to the database).
