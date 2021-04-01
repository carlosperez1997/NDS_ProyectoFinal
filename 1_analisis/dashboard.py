import dash
import dash_core_components as dcc 
import dash_html_components as html
import dash_table

# DataFrame y matrices
import numpy as np 
import pandas as pd

import os

# Visualizacion
import matplotlib.pyplot as plt 
import seaborn as sns
import folium
import plotly.express as px
import plotly.graph_objects as go

pd.options.display.float_format = '{:,.2f}'.format

from dash.dependencies import Input, Output, State

import funciones as f

app = dash.Dash(__name__)

intro_string = '''En esta página se presenta un dashboard con un análisis de la empresa EasyMoney. Se representan varias gráficas, métricas y números.'''

html_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css" integrity="sha384-UHRtZLI+pbxtHCWp1t77Bi1L4ZtiqrqD80Kn4Z8NTSRyMA2Fd33n5dQ8lWUE00s/" crossorigin="anonymous">
        <link rel="stylesheet" href="css/style.css">
    <style>
        @import url('https://fonts.googleapis.com/css?family=Roboto');
        
    </style>
    </head>
    <body id="home">
        <!-- Navbar -->
        <nav id="navbar">
            <h1 class="logo">
            <span class="text-primary"> easy</span>Money
            </h1>
            <ul>
            <li><a href="#analisis"> Análisis - Global </a></li>
            <li><a href="#productos">  Análisis - Productos </a></li>
            <li><a href="#segmentation"> Segmentación </a></li>
            <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div>My Custom footer</div>
    </body>
</html>
'''

# Leemos data
altas_df, bajas_df, productos_exist_df = f.read_data()

# Tipos de producto y su coste
products_dict = {"short_term_deposit":"ahorro e inversión", "loans":"financiación", "mortgage":"financiación", 
    "funds":"ahorro e inversión", "securities":"ahorro e inversión", "long_term_deposit":"ahorro e inversión", 
    "em_account_pp":"cuenta", "credit_card":"financiación", "payroll_account":"cuenta", 
    "emc_account":"cuenta", "debit_card":"financiación", "em_account_p":"cuenta", "em_acount":"cuenta"}

cost_product = {'cuenta':10, 'ahorro e inversión':40, 'financiación':60}

# Ingresos de cada tipo
ingresos_df, ahorros_df, financiacion_df, cuentas_df = f.obtencion_ingresos(altas_df, products_dict, cost_product)

# Resumen con stacked bar horizonal chart
fig1 = f.fig_resumen_mes(financiacion_df, ahorros_df, cuentas_df)
fig1.update_layout(height=200)

# Ingresos totales
ingresos_total = round(ingresos_df.sum(axis=1)['2019-05-28'])

# Ingresos de todos los productos
fig2 = f.fig_ingresos_totales(ingresos_df, ahorros_df, cuentas_df, financiacion_df)
fig2.update_layout(height=500)

# Crecimiento grafica
fig31, ingresos_rate = f.fig_crecimiento(ingresos_df)
growth_rate = round(ingresos_rate[ingresos_rate['pk_partition'] == '2019-05-28']['rate'].values[0]*100)/100

fig32 = f.polar_ingresos(ingresos_df)

# Altas y bajas de todos los productos
altas_df, bajas_df, productos_exist_df = f.read_data()

prod_ahorros, prod_financiacion, prod_cuentas = f.tipos_producto(productos_exist_df, products_dict)
altas_ahorros, altas_financiacion, altas_cuentas = f.tipos_producto(altas_df, products_dict)
bajas_ahorros, bajas_financiacion, bajas_cuentas = f.tipos_producto(bajas_df, products_dict)

fig4 = f.tipo_producto_totales(altas_df, altas_ahorros, altas_financiacion, altas_cuentas)
fig4.update_layout(yaxis_title='Número de altas')

fig5 = f.tipo_producto_totales(bajas_df, bajas_ahorros, bajas_financiacion, bajas_cuentas)
fig5.update_layout(yaxis_title='Número de bajas')

fig4.update_layout(height=500)
fig5.update_layout(height=500)


app.index_string = html_string

app.layout = html.Div(className="main_container", 
    children=[ 
    # Titulo
    html.Div(
        className="header",
        children=[
            html.Div('Análisis - Dashboard', className="app-header--title")
        ]
    ),
    # Introduccion
    html.Div(
        id="intro",
        children = [ intro_string
        ]
    ),
    # Links a codigo
    html.Div(
        className="link_github",
        children = ['Link a Github para ver el código'
        ]
    ),
    # Resumen global ()
    html.Div(
        children=html.Div([
            html.H2('Resumen global')
        ])
    ),
    # Ingresos totales
    html.Div(
        children=html.Div(id = "total", children=[
            html.H3( 'Ingresos este mes: {} €'.format(str(ingresos_total)))
        ])
    ),
    html.Div(
        dcc.Graph(
            figure = fig1
        )
    ),
    
    html.Div(
        children = [
            html.H3('Evolución de Ingresos Mensuales'),
            dcc.Graph(
                figure = fig2
            )
        ]
    ),
    # DIV 1: Crecimiento
    # DIV 2: Polar plot
    html.Div( # Div izda
        children = [
            html.H3('Crecimiento mensual'),
            html.H4( 'Ultimo mes: {} %'.format(growth_rate) ),
            dcc.Graph(
                figure = fig31
            )
        ],
        style={'width': '33%', 'display': 'inline-block'}
    ), # parentesis Div izda

    html.Div( # Div medio
        children = [
            html.H3('Ingresos mensuales'),
            dcc.Graph(
                figure = fig32
            )
        ],
        style={'width': '33%', 'display': 'inline-block'}
    ), # parentesis Div medio
    html.Div( # Div dcha
        children = [
            html.H3('Ingresos mensuales'),
            html.H3('Ingresos mensuales'),
            html.H3('Ingresos mensuales')
        ],
        style={'width': '33%', 'display': 'inline-block'}
    ), # parentesis Div dcha

    # DIV 1: Bajas
    # DIV 2: Altas 
    html.Div( # Div izda
        children = [
            html.H3('Evolución de Altas de Productos'),
            dcc.Graph(
                figure = fig4
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}
    ), # parentesis Div izda

    html.Div( # Div dcha
        children = [
            html.H3('Evolución de Bajas de Productoss'),
            dcc.Graph(
                figure = fig5
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}
    ), # parentesis Div dcha

    # Tipos de productos
    html.Div(id='dropdown_tipo',
        children=html.Div([
            html.H2('Tipo de Productos'),
            html.P('Seleccione un tipo de producto: ', style={'width': '30%', 'display': 'inline-block', 'text-align': 'right'}),
            dcc.Dropdown(id='dropdown_tipo_select',
            options=[
                {'label': 'Ahorro e inversión', 'value': 'ahorros'},
                {'label': 'Financiación', 'value': 'financiacion'},
                {'label': 'Cuentas', 'value': 'cuentas'}
            ],value='cuentas', style={'width': '70%', 'display': 'inline-block'})
        ])
    ),

    # DIV 1: Ingresos
    # DIV 2: Bajas 
    # DIV 3: Churn Ratio 
    html.Div( # Div izda
        children = [
            html.H3('Evolución de Ingresos'),
            dcc.Graph(
                id='graph61'
            )
        ],
        style={'width': '33%', 'display': 'inline-block'}
    ), # parentesis Div izda

    html.Div( # Div medio
        children = [
            html.H3('Evolución de Altas de Productoss'),
            dcc.Graph(
                id='graph62'
            )
        ],
        style={'width': '33%', 'display': 'inline-block'}
    ), # parentesis Div medio

    html.Div( # Div dcha
        children = [
            html.H3('Churn Ratio'),
            dcc.Graph(
                id='graph63'
            )
        ],
        style={'width': '33%', 'display': 'inline-block'}
    ), # parentesis Div dcha

    dcc.Dropdown(
            id='opt-dropdown',
            placeholder="Selecciona un producto",
    ),
    html.H1(
        id='seleccion',
    )
        

])


@app.callback(
    Output('graph61', 'figure'),
    Output('graph62', 'figure'),
    Output('graph63', 'figure'),
    Output('opt-dropdown', 'options'),
    Input('dropdown_tipo_select', 'value')
)
def update_output(tipo_producto):
    if tipo_producto == 'ahorros':
        tipo_ingresos = ahorros_df.copy(deep=True)
        tipo_productos = prod_ahorros.copy(deep=True)
        tipo_altas = altas_ahorros.copy(deep=True)
        tipo_bajas = bajas_ahorros.copy(deep=True)
    elif tipo_producto == 'financiacion':
        tipo_ingresos = financiacion_df.copy(deep=True)
        tipo_productos = prod_financiacion.copy(deep=True)
        tipo_altas = altas_financiacion.copy(deep=True)
        tipo_bajas = bajas_financiacion.copy(deep=True)
    elif tipo_producto == 'cuentas':
        tipo_ingresos = cuentas_df.copy(deep=True)
        tipo_productos = prod_cuentas.copy(deep=True)
        tipo_altas = altas_cuentas.copy(deep=True)
        tipo_bajas = bajas_cuentas.copy(deep=True)    
    

    fig1 = f.fig_ingresos_tipo(tipo_ingresos)
    fig1.update_layout(height=400)
    fig2 = f.fig_ingresos_tipo(tipo_bajas)
    fig2.update_layout(height=400)
    fig3 = f.fig_churn_plot(tipo_productos, tipo_altas, tipo_bajas)
    fig3.update_layout(height=400)

    opts = list(tipo_ingresos.columns)
    options=[{'label':opt, 'value':opt} for opt in opts]
   
    #value = options[0]

    return fig1, fig2, fig3, options#, value

@app.callback(
    Output('seleccion', 'children'),
    Input('opt-dropdown', 'value'))
def set_display_children(selected_value):
    return 'you have selected {} option'.format(selected_value)


if __name__ == '__main__':
    app.run_server(debug = True)