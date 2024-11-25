from dash import State, html, Input, Output, callback, callback_context, dcc
import dash_bootstrap_components as dbc
import requests
import pandas as pd
from utils.api import API
from components.export_to_excel import export_button

# Pagination constants
# ROWS_PER_PAGE = 10  # Number of rows to display per page
rows_selector = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("5", id="btn-5"),
        dbc.DropdownMenuItem("10", id="btn-10"),
        dbc.DropdownMenuItem("20", id="btn-20"),
        dbc.DropdownMenuItem("50", id="btn-50"),
        dbc.DropdownMenuItem("100", id="btn-100"),
    ],
    id="rows_selector",
    label="Products per page",
)


# Function to fetch data from the backend
def fetch_data(page, per_page):
    # Replace with your actual backend API URL
    url = f"{API}/records"
    response = requests.get(url, {"page": f"{page}", "per_page": f"{per_page}"})
    response.raise_for_status()  # Raise an error if the request fails
    return response.json()


# Generate a dbc.Table from data
def generate_table(data, page):
    # Convert JSON to a Pandas DataFrame for convenience
    print(data)

    # Create table header
    header = [html.Th(col) for col in data.columns]

    # Create table rows
    rows = [
        html.Tr([html.Td(data.iloc[i][col]) for col in data.columns])
        for i in range(len(data))
    ]

    # Return a dbc.Table
    return dbc.Table(
        # Combine header and rows
        [html.Thead(html.Tr(header)), html.Tbody(rows)],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
    )


# Initial layout
product_table = html.Div(
    [
        html.H1("Product Table"),
        html.Div(rows_selector),
        html.Div(id="assets-table"),
        # Pagination Controls
        html.Div(
            id="pagination-contents",
        ),
        # Export to Excel Button
        export_button,
        # Hidden data storage
        dcc.Store(id="data-store", storage_type="session"),  # To store fetched data
    ]
)


# Callback to select rows-per-page
@callback(
    [
        Output("data-store", "data"),
        Output("data-store", "rows_per_page"),
        Output("data-store", "current_page"),
        Output("data-store", "total_pages"),
        Output("pagination-contents", "children"),
    ],
    [
        Input("btn-5", "n_clicks"),
        Input("btn-10", "n_clicks"),
        Input("btn-20", "n_clicks"),
        Input("btn-50", "n_clicks"),
        Input("btn-100", "n_clicks"),
    ],
    [State("data-store", "current_page")],
)
def display(btn1, btn2, btn3, btn4, btn5, current_page):
    id_lookup = {"btn-5": 5, "btn-10": 10, "btn-20": 20, "btn-50": 50, "btn-100": 100}
    ctx = callback_context
    button_id = ctx.triggered_id
    print(button_id)
    if (button_id is None) or not ctx.triggered:
        # if neither button has been clicked, return "Not selected"
        current_page = 1
        button_id = "btn-5"
    else:  # needed for when page is already rendered
        current_page = current_page
        button_id = button_id

    response = fetch_data(current_page, id_lookup[button_id])
    current_page = response["current_page"]
    total_pages = response["total_pages"]
    # this gets the id of the button that triggered the callback
    return (
        response["data"],
        id_lookup[button_id],
        current_page,
        total_pages,
        dbc.Pagination(
            id="pagination",
            active_page=current_page,
            max_value=total_pages,
        ),
    )


# 1- Callback to fetch and send to store as JSON
# @callback(
#     [
#         Output("data-store", "data"),
#         Output("data-store", "current_page"),
#         Output("data-store", "total_pages"),
#         Output("pagination-contents", "children"),
#     ],
#     [
#         Input("url", "pathname"),
#     ],
#     [State("data-store", "rows_per_page")],
#     prevent_initial_control=False,
# )
# def update_table_on_load(pathname, rows_per_page):
#     # page = 1  # Default to page 1 if no active page
#     response = fetch_data(1, rows_per_page)
#     current_page = response["current_page"]
#     total_pages = response["total_pages"]

#     return (
#         response["data"],
#         {"current_page": current_page},
#         {"total_pages": total_pages},
#         dbc.Pagination(
#             id="pagination",
#             active_page=current_page,
#             max_value=total_pages,
#         ),
#     )


# 2- Proper pagination callback
@callback(
    Output("assets-table", "children"),
    [Input("pagination", "active_page")],
    [
        State("data-store", "data"),
        State("data-store", "current_page"),
        State("data-store", "total_pages"),
        State("data-store", "rows_per_page"),
    ],
    prevent_initial_call=False,  # Allow initial trigger
)
def display_table_page(active_page, data, current_page, total_pages, rows_per_page):
    if not data:
        return dbc.Alert(
            "No data available to display.", color="warning"
        ), "Page 0 of 0"

    try:
        # Load data from JSON
        df = pd.json_normalize(data)
    except ValueError:
        return dbc.Alert(
            "Failed to parse data. Check backend response.", color="danger"
        ), "Page 0 of 0"

    ctx = callback_context
    trigger = ctx.triggered[0]["prop_id"]
    print(trigger)

    if "active_button" in trigger and current_page > 1:
        active_page -= 1
    elif "active_button" in trigger and current_page < total_pages:
        active_page += 1

    df = pd.json_normalize(fetch_data(active_page, rows_per_page)["data"])
    # Generate table for the current page
    table = generate_table(df, page=active_page)

    return table
