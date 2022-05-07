import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State

from settings import config, about
from python.data import Data
from python.plot import Plot

# Get Data
data = Data()
data.get_data()

# Instantiate plot object
plot = Plot()

# Create app instance
app = Dash(name=config.name, assets_folder=config.root+"/application/static", external_stylesheets=[dbc.themes.LUX, config.fontawesome])
app.title = config.name

# Navbar
navbar = dbc.Nav(className="nav nav-pills", children=[
    # Logo / Home
    dbc.NavItem(html.Img(src=app.get_asset_url("logo.png"), height="40px")),
    # About
    dbc.NavItem(html.Div([
        dbc.NavLink("About", href="/", id="about-popover", active=False),
        dbc.Popover(id="about", is_open=False, target="about-popover", children=[
            dbc.PopoverHeader("Study Details"), dbc.PopoverBody(about.txt)
        ])
    ])),
    # Links
    dbc.DropdownMenu(label="Links", nav=True, children=[
        dbc.DropdownMenuItem([html.I(className="fa fa-linkedin"), "  Contact"], href=config.contacts, target="_blank"), 
        dbc.DropdownMenuItem([html.I(className="fa fa-github"), "  Code"], href=config.code, target="_blank")
    ])
])

# App layout
app.layout = dbc.Container(fluid=True, children=[
    # Top
    html.H1(config.name, id="nav-pills", style={'padding-top':'.3em'}),
    navbar,
    html.Br(),html.Br(),html.Br(),
    # Body
    dbc.Row([
        # Input + Panel
        dbc.Col(md=3, children=[
            html.H4("Select Law Passed"),
            dcc.Dropdown(id="law", options=[{"label":y,"value":x} for x,y in list(zip(data.year_columns,data.year_column_labels))], value="debtfree"),
            html.Br(),html.Br(),html.Br(),
            html.Div(id="desc-panel")
        ]),
        # Plots
        dbc.Col(md=9, children=[
            dbc.Col(html.H4("Year Law passed per State"), width={"size":6,"offset":3}), 
            dbc.Tabs(className="nav nav-pills", children=[
                dbc.Tab(dcc.Graph(id="plot-color", figure="plot-color"), label="Color"),
                dbc.Tab(dcc.Graph(id="plot-bw", figure="plot-bw"), label="Black & White"),
            ])
        ])
    ])
])

# Logic for the about navitem-popover
@app.callback(output=Output("about","is_open"), inputs=[Input("about-popover","n_clicks")], state=[State("about","is_open")])
def about_popover(n, is_open):
    if n:
        return not is_open
    return is_open
@app.callback(output=Output("about-popover","active"), inputs=[Input("about-popover","n_clicks")], state=[State("about-popover","active")])
def about_active(n, active):
    if n:
        return not active
    return active

# Plot color choropleth
@app.callback(output=Output("plot-color","figure"), inputs=[Input("law","value")]) 
def plot_color(law):
    fig = plot.plot_choro(None,'RdPu_r',law)
    return fig

# Plot black & white choropleth
@app.callback(output=Output("plot-bw","figure"), inputs=[Input("law","value")]) 
def plot_bw(law):
    fig = plot.plot_choro(None,[[0.0, "rgb(70,70,70)"],[1.0, "rgb(255, 255, 255)"]],law)
    return fig

# Render desc panel
@app.callback(output=Output("desc-panel","children"), inputs=[Input("law","value")])
def render_output_panel(law):
    law_label = data.law_dict[law]
    law_desc = data.desc_dict[law]
    panel = html.Div([
        html.H4(law_label),
        dbc.Card(body=True, className="text-white bg-primary", children=[
            html.Div(law_desc, style={"color":"white",'font-size':'1.5em'}),
        ])
    ])
    return panel