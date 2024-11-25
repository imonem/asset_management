import dash_bootstrap_components as dbc
from dash import html

from components.color_switch import color_mode_switch

LOGO = "https://gs1eg.org/wp-content/uploads/2020/05/GS1_Egypt_2014-12-17.png"


search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button("Search", color="primary", className="mx-2", n_clicks=0),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

actions_items = [
    dbc.DropdownMenuItem("Home", href="/"),
    dbc.DropdownMenuItem("Create", href="/create_one"),
    dbc.DropdownMenuItem("Bulk Update", href="/bulk_update"),
    dbc.DropdownMenuItem("Export", href="/export"),
    dbc.DropdownMenuItem("Reports", href="/reports"),
]

actions_dropdownmenu = dbc.Row(
    [
        dbc.DropdownMenu(
            actions_items,
            label="Actions",
            in_navbar=True,
            color="primary",
            align_end=True,
            # className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
        ),
    ]
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO, height="30px")),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "Asset Managament Application", className="ms-2"
                            )
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="#",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                children=[search_bar, actions_dropdownmenu],
                id="navbar-collapse",
                class_name="me-2",
                is_open=False,
                navbar=True,
            ),
            color_mode_switch,
        ]
    ),
    color="",
    dark="",
)
