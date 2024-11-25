import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__, path="/reports")

layout = html.Div(
    [
        html.H2("Reports placeholder"),
        dbc.Col(
            children=[
                dbc.Button(
                    "Export to Excel",
                    id="export-excel",
                    color="success",
                    class_name="me-2",
                ),
                dbc.Button(
                    "Export to CSV", id="export-csv", color="primary", class_name="me-2"
                ),
            ],
            class_name=["column-gap-3"],
        ),
        html.Div(id="export-output"),
    ]
)

# Callbacks for export functionality would go here.
