import dash
import dash_core_components as dcc 
import dash_html_components as html
import dash_table

# DataFrame y matrices
import numpy as np 
import pandas as pd

from apps import dashboard_app
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    elif pathname == '/apps/dashboard':
        return dashboard_app.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug = True)