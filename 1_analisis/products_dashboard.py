import dash
import dash_core_components as dcc 
import dash_html_components as html
#import dash_table
from dash_table import DataTable

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
import product_functions as fp

dir_path = '/Users/carlosperezricardo/Documents/data/'

app = dash.Dash(__name__)

intro_string = '''Este dashboard es para un solo producto, en él puedes seleccionar un producto y te aparecerán las figuras de altas, bajas, churn rate, ingresos, combinaciones de 2 productos(clientes que han comprado X también compran Y), permanencia y antigüedad de los clientes y comparaciones en cuanto a edades y salarios de los clientes de este producto con otros productos'''

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

paises_code = {'ES': ['ES','Spain'], 'GB':['EU','United Kingdom'], 'US':['NA','US'], 
    'FR':['EU','France'], 'CH':['EU','Switzerland'], 'DE':['EU','Germany'], 'BE':['EU','Belgium'], 
    'BR':['SA','Brazil'], 'VE':['SA','Venezuela'], 'MX':['SA','Mexico'], 'AR':['SA','Argentina'], 
    'IE':['EU','Ireland'], 'PL':['EU','Poland'], 'IT':['EU','Italy'], 'AT':['EU','Austria'], 
    'SE':['EU','Sweden'], 'CL':['SA','Chile'], 'MA':['AF','Morocco'], 'CO':['SA','Colombia'], 
    'DZ':['AF','Algeria'], 'SN':['AF','Senegal'], 'ET':['AF','Ethiopia'], 'RU':['EU','Russia'], 
    'GA':['AF','Gambia'], 'SA':['AS','Saudi Arabia'], 'MR':['AF','Mautirania'], 'HU':['EU','Hungary'], 
    'JM':['SA','Jamaica'], 'CM':['AF','Cameroon'], 'CI':['AF',"Cote d'Ivoire"], 'RO':['EU','Romania'], 
    'PE':['SA','Peru'], 'DO':['SA','Dominican Republic'], 'QA':['AS','Qatar'], 'PT':['EU','Portugal'], 
    'LU':['EU','Luxembourg'], 'DJ':['AF','Djibouti'], 'GT':['SA','Guatemala'], 'CN':['AS','China'], 
    'NO':['EU','Norway'], 'CA':['NA','Canada']}

spanish_regions_code = {1:['Elciego', 'País Vasco'], 2:['Albacete', 'Castilla-La Mancha'], 
3:['Alicante/Alacant', 'Com. Valenciana'],4:['Almería','Andalucía'],
5:['Ávila','Castilla y León'], 6:['Badajoz','Extremadura'],	
7:['Palma','Islas Baleares'], 8:['Barcelona','Cataluña'],
9:['Burgos','Castilla y León'], 10: ['Cáceres','Extremadura'], 11: ['Cádiz','Andalucía'], 12: ['Castellón de la Plana/Castelló de la Plana','Com. Valenciana'], 13: ['Ciudad Real','Castilla-La Mancha'], 14: ['Córdoba','Andalucía'], 15: ['Coruña (A)','Galicia'], 16: ['Cuenca','Castilla-La Mancha'], 17: ['Girona','Cataluña'], 18: ['Granada','Andalucía'], 19: ['Guadalajara','Castilla-La Mancha'], 20: ['Donostia-San Sebastián','País Vasco'], 21: ['Huelva','Andalucía'], 22: ['Huesca','Aragón'], 23: ['Jaén','Andalucía'], 24: ['León','Castilla y León'], 25: ['Lleida','Cataluña'], 26: ['Logroño','La Rioja'], 27: ['Lugo','Galicia'], 28: ['Madrid','Madrid'], 29: ['Málaga','Andalucía'], 30: ['Murcia','Murcia'], 31: ['Pamplona/Iruña','Com. de Navarra'], 32: ['Ourense','Galicia'], 33: ['Oviedo','Princ. de Asturias'], 34: ['Palencia','Castilla y León'], 35: ['Palmas de Gran Canaria (Las)','Islas Canarias'], 36: ['Pontevedra','Galicia'], 37: ['Salamanca','Castilla y León'], 38: ['Santa Cruz de Tenerife','Islas Canarias'], 39: ['Santander','Cantabria'], 40: ['Segovia','Castilla y León'], 41: ['Sevilla','Andalucía'], 42: ['Soria','Castilla y León'], 43: ['Tarragona','Cataluña'], 44: ['Teruel','Aragón'], 45: ['Toledo','Castilla-La Mancha'], 46: ['Valencia','Com. Valenciana'], 47: ['Valladolid','Castilla y León'], 48: ['Bilbao','País Vasco'], 49: ['Zamora','Castilla y León'], 50: ['Zaragoza','Aragón'], 51: ['Ceuta','Ceuta y Melilla'], 52: ['Melilla','Ceuta y Melilla']}

list_products = ["short_term_deposit", "loans", "mortgage", "funds", "securities", "long_term_deposit", "em_account_pp", "credit_card", "payroll_account", "emc_account", "debit_card", "em_account_p", "em_acount"]

dropdown_opts = []

for prod in list_products:
    dropdown_opts.append( {'label': prod, 'value':prod } )

# Tipos de producto y su coste
products_dict = {"short_term_deposit":"ahorro e inversión", "loans":"financiación", "mortgage":"financiación", 
    "funds":"ahorro e inversión", "securities":"ahorro e inversión", "long_term_deposit":"ahorro e inversión", 
    "em_account_pp":"cuenta", "credit_card":"financiación", "payroll_account":"cuenta", 
    "emc_account":"cuenta", "debit_card":"financiación", "em_account_p":"cuenta", "em_acount":"cuenta"}

cost_product = {'cuenta':10, 'ahorro e inversión':40, 'financiación':60}

# Altas y bajas de todos los productos
altas_df, bajas_df, productos_exist_df = f.read_data()

# Ingresos de cada tipo
ingresos_df, ahorros_df, financiacion_df, cuentas_df = f.obtencion_ingresos(altas_df, products_dict, cost_product)

prod_ahorros, prod_financiacion, prod_cuentas = f.tipos_producto(productos_exist_df, products_dict)
altas_ahorros, altas_financiacion, altas_cuentas = f.tipos_producto(altas_df, products_dict)
bajas_ahorros, bajas_financiacion, bajas_cuentas = f.tipos_producto(bajas_df, products_dict)

# permanencias
first_partition = '2018-01-28'
last_partition = '2019-05-28'

products = pd.read_csv(dir_path+'products_df.csv', encoding='utf-8')
products.drop(columns=['Unnamed: 0'], inplace=True)
products_sorted = products.sort_values(by=['pk_cid', 'pk_partition'])
products_sorted['pk_partition'] = pd.to_datetime(products_sorted['pk_partition'])

first_buyers = pd.read_csv(dir_path+'first_buyers.csv')
most_recent_buyers = first_buyers[ first_buyers['pk_partition'] == last_partition ]




#[ ahorros_df['pk_partition'] == last_partition ]['loans']





app.index_string = html_string

app.layout = html.Div(className="main_container", 
    children=[ 
    # Titulo
    html.Div(
        className="header",
        children=[
            html.Div('Análisis de productos', className="app-header--title")
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
    # Productos
    html.Div(id='dropdown_tipo',
        children=html.Div([
            html.P('Seleccione el producto: ', style={'width': '30%', 'display': 'inline-block', 'text-align': 'right'}),
            dcc.Dropdown(id='dropdown_tipo_select',
            options= dropdown_opts, 
            value='loans', style={'width': '70%', 'display': 'inline-block'})
        ])
    ),
    html.Div(
        html.Ul(children = [
            # ingresos mensuales
            html.Li( className='summary_window',
                children = [
                    html.Div( className='text', children=[
                    html.H4('Ingresos Mensuales (€):')
                    ]),
                    html.Div( className='value', children=[
                            html.P( id='ingresos')
                    ]),
                    html.Div( className='flecha', children=[
                        html.P('▲') # U+25B2
                    ]),
                    html.Div( className='crecimiento', children=[
                            html.P('3%')  
                    ]),
            ]),
            # Nuevos Clientes
            html.Li( className='summary_window',
                children = [
                    html.Div( className='text', children=[
                    html.H4('Nuevos Clientes:')
                    ]),
                    html.Div( className='value', children=[
                            html.P( id='nuevos_clientes' )
                    ]),
                    html.Div( className='flecha', children=[
                        html.P('▲') # U+25B2
                    ]),
                    html.Div( className='crecimiento', children=[
                            html.P('3%')  
                    ]),
            ]),
            # Clientes Activos
            html.Li( className='summary_window',
                children = [
                    html.Div( className='text', children=[
                    html.H4('Clientes Activos:')
                    ]),
                    html.Div( className='value', children=[
                            html.P( id='clientes_activos' )
                    ]),
                    html.Div( className='flecha', children=[
                        html.P('▲') # U+25B2
                    ]),
                    html.Div( className='crecimiento', children=[
                            html.P('3%')  
                    ]),
            ]),
        ]),
    ),
    html.Div( 
        children=[ html.H3('Altas y bajas de productos'), 
            dcc.Graph( id='fig_altas_bajas' )
        ], style={'width': '33%', 'display': 'inline-block'}
    ), 
    html.Div( 
        children=[ html.H3('Ingresos'), 
            dcc.Graph( id='fig_ingresos' )
        ], style={'width': '33%', 'display': 'inline-block'}
    ), 
    html.Div( 
        children=[ html.H3('Churn Rate'),
            html.H4('Churn rate medio:'),
            html.P( id='mean_churn' ),
            dcc.Graph( id='fig_churn' )
        ], style={'width': '33%', 'display': 'inline-block'}
    ),
    html.Div( 
        children=[ html.H3('Permanencia'),
            html.H4( id='mean_perm'),
            dcc.Graph( id='fig_permanencias' )
        ], style={'width': '33%', 'display': 'inline-block'}
    ),
    html.Div( 
        children=[ html.H3('Antigüedad'),
            html.H4( id='mean_antig'),
            dcc.Graph( id='fig_antiguedades' )
        ], style={'width': '33%', 'display': 'inline-block'}
    ),
    html.Div( 
        children=[ html.H3('Canales de entrada'),
            dcc.Graph( id='fig_canal' )
        ], style={'width': '33%', 'display': 'inline-block'}
    ),
    html.Div( 
        children=[ html.H3('Regiones España'),
            dcc.Graph( id='fig_spain' )
        ], style={'width': '33%', 'display': 'inline-block'}
    ),
    html.Div( 
        children=[ html.H3('Extranjero'),
            dcc.Graph( id='fig_abroad' )
        ], style={'width': '33%', 'display': 'inline-block'}
    ),
    html.Div( 
        children=[ html.H3('Edades'),
            dcc.Graph( id='fig_edades' )
        ], style={'width': '50%', 'display': 'inline-block'}
    ),
    html.Div( 
        children=[ html.H3('Salarios'),
            dcc.Graph( id='fig_salarios' )
        ], style={'width': '50%', 'display': 'inline-block'}
    ),
    html.Div( id='two_pack',
        children=[ html.H3('Combinaciones de 2 productos'),
            html.H4('Clientes que han comprado este producto también han comprado:'),
            DataTable(
            id='twopack_table',
            ),
            html.P(children=['Definición de las columnas:'], className='bold'),
            html.P('Producto Referencia; Producto Complementario; Numero de Clientes con ambos productos; Numero de Clientes con el producto referencia; Numero de Clientes con el producto complementario; % de clientes con el producto referencia con el producto complementario'),
        ], style={'width': '55%', 'margin':'auto'}
    )

        

])


@app.callback(
    Output('ingresos', 'children'),
    Output('nuevos_clientes', 'children'),
    Output('clientes_activos', 'children'),
    Output('fig_altas_bajas', 'figure'),
    Output('fig_ingresos', 'figure'),
    Output('mean_churn', 'children'),
    Output('fig_churn', 'figure'),
    Output('mean_perm', 'children'),
    Output('fig_permanencias', 'figure'),
    Output('mean_antig', 'children'),
    Output('fig_antiguedades', 'figure'),
    Output('fig_canal', 'figure'),
    Output('fig_spain', 'figure'),
    Output('fig_abroad', 'figure'),
    Output('fig_salarios', 'figure'),
    Output('fig_edades', 'figure'),
    Output("twopack_table", "data"),
    Output("twopack_table", "columns"),
    Input('dropdown_tipo_select', 'value')
)
def update_output(producto):
     
    # Ingresos, nuevos clientes y clientes activos 
    ingresos = str( int(altas_df.loc[last_partition][producto]) )
    nuevos_clientes = str( most_recent_buyers.groupby(producto)['pk_cid'].count()[0] )
    
    clientes_activos = str( 1000 )
    print( ingresos_df.loc[last_partition][producto] )

    # Altas y bajas de productos
    fig_altas_bajas, altas_, bajas_ = fp.altas_bajas_producto(altas_df[1:], bajas_df[1:], producto)
   
    # Ingresos
    tipo_producto = products_dict[producto]

    if tipo_producto == 'ahorro e inversión':
        tipo_ingresos = ahorros_df.copy(deep=True)
        tipo_productos = prod_ahorros.copy(deep=True)
        tipo_altas = altas_ahorros.copy(deep=True)
        tipo_bajas = bajas_ahorros.copy(deep=True)
    elif tipo_producto == 'financiación':
        tipo_ingresos = financiacion_df.copy(deep=True)
        tipo_productos = prod_financiacion.copy(deep=True)
        tipo_altas = altas_financiacion.copy(deep=True)
        tipo_bajas = bajas_financiacion.copy(deep=True)
    elif tipo_producto == 'cuenta':
        tipo_ingresos = cuentas_df.copy(deep=True)
        tipo_productos = prod_cuentas.copy(deep=True)
        tipo_altas = altas_cuentas.copy(deep=True)
        tipo_bajas = bajas_cuentas.copy(deep=True)   
    
    fig_ingresos = f.fig_ingresos_tipo(tipo_ingresos)
    fig_ingresos.update_layout(height=400)

    # Churn 
    fig_churn, churn_text = fp.obtener_churn (tipo_productos, tipo_altas, tipo_bajas, producto)

    # Permanencias
    fig_permanencias, perm_text = fp.permanencias(products_sorted, producto, first_partition, last_partition)

    # Permanencias
    fig_antiguedades, antig_text = fp.antiguedad(products_sorted, producto, first_partition, last_partition)

    two_pack = fp.two_combination(producto, products)
    data = two_pack.to_dict('records')
    columns = [{"name": i, "id": i} for i in two_pack.columns]

    #Salarios, Edades y Paises
    fig_salarios, fig_edades, fig_spain, fig_abroad, fig_canal = fp.fig_salarios_edades_paises( products_dict, producto, dir_path, spanish_regions_code, paises_code)

    return ingresos, nuevos_clientes, clientes_activos, fig_altas_bajas, fig_ingresos, churn_text, fig_churn, perm_text, fig_permanencias, antig_text, fig_antiguedades, fig_canal, fig_spain, fig_abroad, fig_salarios, fig_edades, data, columns


if __name__ == '__main__':
    app.run_server(debug = True)