import dash
from dash import dcc, html
from components.product_table import product_table

dash.register_page(__name__, path="/")

pathname = "/"

markdown_message = """
# Welcome to GS1 Egypt Asset Management Interface

Please select an action from the `Actions` menu to begin.

If you have questions related to usage, please reach out to me at [amr.nabeel@gs1eg.org](mailto:amr.nabeel@gs1eg.org)
"""

layout = html.Div(
    [
        dcc.Location(id="url"),  # This is critical for pathname tracking
        dcc.Markdown(markdown_message),
        html.Hr(),
        product_table,
    ]
)
