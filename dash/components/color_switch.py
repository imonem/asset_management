import dash_bootstrap_components as dbc
from dash import Input, Output, clientside_callback, html

color_mode_switch = html.Span(
    [
        dbc.Label(class_name="fa fa-moon", html_for="switch"),
        dbc.Switch(
            id="switch", value=True, class_name="d-inline-block ms-1", persistence=True
        ),
        dbc.Label(class_name="fa fa-sun", html_for="switch"),
    ]
)

clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');
       return window.dash_clientside.no_update
    }
    """,
    Output("switch", "id"),
    Input("switch", "value"),
)
