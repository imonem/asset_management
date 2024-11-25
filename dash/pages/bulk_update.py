import dash
from dash import dcc, html

dash.register_page(__name__, path="/bulk_update")

layout = html.Div(
    [
        html.H2("Bulk Update Products"),
        dcc.Upload(
            id="upload-file",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
        ),
        html.Div(id="upload-output"),
    ]
)

# Callbacks to process uploaded file and update the database would go here.
