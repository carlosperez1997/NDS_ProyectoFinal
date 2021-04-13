import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

import dash
import dash_core_components as dcc 
import dash_html_components as html

import plotly.express as px
import plotly.graph_objects as go

pd.options.display.float_format = '{:,.2f}'.format

def altas_bajas_producto (altas, bajas, producto):
  altas_ = altas[['pk_partition',producto]]
  bajas_ = bajas[['pk_partition',producto]]

  fig = go.Figure()
 
  fig.add_trace(go.Scatter(x=altas_["pk_partition"], y=altas_[producto], name='Altas'))
  fig.add_trace(go.Scatter(x=bajas_["pk_partition"], y=bajas_[producto], name='Bajas'))

  if altas_.max()[producto] > bajas_.max()[producto]:
    max_value = altas_.max()[producto]
  else:
    max_value = bajas_.max()[producto]
  fig.update_yaxes(range=[0, max_value*1.05])
  fig.update_layout(yaxis_title='Productos de'+producto)
  fig.update_layout(legend=dict(
      orientation="h", yanchor="bottom", y=1.02,
      xanchor="center", x=0.5,
      font=dict(family="Courier",size=14,color="black")
  ))

  return fig, altas_, bajas_


def vc_to_dict(prod_df, col, imax):
    dicc = {}
    result = prod_df[col].value_counts().sort_index()

    for i in range(1,imax+1):
        if i in result.index:
            dicc[i] = result[i] 
        else:
            dicc[i] = 0   
            
    return dicc


def dicc_mean(dicc):
  accu = 0
  count = 0
  for key, val in dicc.items():
    accu += (key+1)*val
    count += val

  if count == 0:
    result = 0
  else:
    result = accu/count
  
  return result


def cambiar_duraciones(vector, duraciones):
  new_vector = {}
  for x in duraciones:
    #print(duraciones[x][0])
    for i in range( duraciones[x][0], duraciones[x][1]+1 ):
      if i in vector:
        if x in new_vector:
          new_vector[x] = new_vector[x] + vector[i]
        else:
          new_vector[x] = vector[i]

  return new_vector


def permanencias(permanencias, prod):
    perm = permanencias[prod]

    mean = dicc_mean(perm)
    perm_text = 'Permanencia media: '+str( round(mean*10)/10 )+' meses'

    duraciones = {'1-2 meses':[1,2], '3-6 meses':[3,6], '7-12 meses':[7,12], 'Más de 12 meses':[13,20]}

    new_perm = cambiar_duraciones(perm, duraciones)
    new_perm = pd.DataFrame(new_perm, index=['mes']).T
    new_perm = new_perm.reset_index()

    fig = px.bar(new_perm, x="index", y="mes")
    fig.update_layout(
      yaxis_title='Número de clientes',
      xaxis_title=''
    )
    
    return fig, perm_text


def antiguedad(antiguedades_df, prod):
    antig = antiguedades_df[prod]

    mean = dicc_mean(antig)
    antig_text = 'Antigüedad media: '+str( round(mean*10)/10 )+' meses'

    duraciones = {'1-2 meses':[1,2], '3-6 meses':[3,6], '7-12 meses':[7,12], 'Más de 12 meses':[13,20]}

    new_antig = cambiar_duraciones(antig, duraciones)
    new_antig = pd.DataFrame(new_antig, index=['mes']).T
    new_antig = new_antig.reset_index()

    fig = px.bar(new_antig, x="index", y="mes")
    fig.update_layout(
      yaxis_title='Número de clientes',
      xaxis_title=''
    )

    return fig, antig_text


def obtener_churn (tipo_productos, tipo_altas, tipo_bajas, prod):
    churn_local = tipo_productos[['pk_partition',prod]]
    churn_local['old'] = churn_local[prod].shift(1)

    churn_local['altas'] = tipo_altas[[prod]]
    churn_local['bajas'] = tipo_bajas[[prod]]
    churn_local['churn_rate'] = churn_local['bajas']/(churn_local['old'] + churn_local['altas'])*100
    churn_local = churn_local[1:]

    churn_local = churn_local.reset_index()
    
    churn_local['churn_rate'].fillna(0, inplace=True) 

    churn_text = str( round(churn_local['churn_rate'][1:].mean()*100)/100 ) + '%'

    fig = px.line(churn_local, x='pk_partition', y='churn_rate')
    
    return fig, churn_text


def combinations_table(combinaciones_df, producto):
  comb = combinaciones_df[ combinaciones_df['producto_1'] == producto ]
  comb.columns = ['Producto ref.','Producto comp.', 'Clientes Ambos', 'Clientes Ref.', 'Clientes Comp.', 'Proporcion' ]

  return comb
  

def fig_spain( df, producto ):
  data = df [ df['producto'] == producto ]
  fig = px.bar(data, x='ciudad', y='ciudad_num')

  return fig


def fig_abroad( df, producto):
  data = df [ df['producto'] == producto ]
  data = data[ data['pais_num'] != 0]
  fig = px.bar(data, x='pais', y='pais_num')

  return fig


def fig_canal( df, producto ):
  data = df [ df['producto'] == producto ]
  data = data[ data['entry_channel_num'] != 0]
  fig = px.bar(data, x='entry_channel', y='entry_channel_num')

  return fig


def fig_salarios_edades_paises( products_dict, prod, dir_path, spanish_regions_code, paises_code):

    socioproductscommercial = obtain_socioproductscommercial(dir_path)
    tipo_prod = products_dict[prod]

    products = []

    for key, val in products_dict.items():
        if val == tipo_prod:
            products.append(key)

    c1 = (socioproductscommercial [products[0]] == 1) 
    c2 = (socioproductscommercial [products[1]] == 1) 
    c3 = (socioproductscommercial [products[2]] == 1) 
    c4 = (socioproductscommercial [products[3]] == 1) 

    if len(products) == 5:
        c5 = (socioproductscommercial [products[4]] == 1) 
    else:
        c5 = (socioproductscommercial [products[0]] == 1) 

    info_product = socioproductscommercial [ c1 | c2 | c3 | c4 | c5 ]
    info_product = info_product.sort_values(['pk_cid','pk_partition'], ascending=False)
    info_product = info_product.groupby('pk_cid').last()

    # Salarios
    fig1 = go.Figure()

    for p in products:
        salary_box = info_product[ info_product[p] == 1 ]['salary'].dropna()
        
        # Use x instead of y argument for horizontal plot
        fig1.add_trace(go.Violin(x=salary_box, name=p))

    # Edades
    fig2 = go.Figure()

    for p in products:
        age_box = info_product[ info_product[p] == 1 ]['age'].dropna()
        
        # Use x instead of y argument for horizontal plot
        fig2.add_trace(go.Box(x=age_box, name=p))

    fig3, fig4, fig5 = paises_channel_clients ( socioproductscommercial, prod, spanish_regions_code, paises_code )

    fig1.update_layout(legend=dict(
      orientation="h", yanchor="bottom", y=1.02,
      xanchor="center", x=0.5,
      font=dict(family="Courier",size=14,color="black")
    ))
    fig2.update_layout(legend=dict(
      orientation="h", yanchor="bottom", y=1.02,
      xanchor="center", x=0.5,
      font=dict(family="Courier",size=14,color="black")
    ))

    return fig1, fig2, fig3, fig4, fig5


def obtain_socioproductscommercial(dir_path):
    sociodemographic_df = pd.read_csv(dir_path+'sociodemographic_df.csv')
    sociodemographic_df.drop('Unnamed: 0', axis=1, inplace=True)
    products_df = pd.read_csv(dir_path+'products_df.csv')
    products_df.drop('Unnamed: 0', axis=1, inplace=True)
    commercial_df = pd.read_csv(dir_path+'commercial_activity_df.csv')
    commercial_df .drop('Unnamed: 0', axis=1, inplace=True)

    socioproducts = pd.merge(sociodemographic_df, products_df, how='inner', on=['pk_cid','pk_partition'])
    socioproductscommercial = pd.merge(socioproducts, commercial_df, how='inner', on=['pk_cid','pk_partition'])

    return socioproductscommercial


def paises_channel_clients ( socioproductscommercial, prod, spanish_regions_code, paises_code):
    # Spain
    info_product_ = socioproductscommercial [ (socioproductscommercial [prod] == 1) ]
    info_product_ = info_product_.sort_values(['pk_cid','pk_partition'], ascending=False)
    info_product_ = info_product_.groupby('pk_cid').last()

    spain = pd.DataFrame(spanish_regions_code).T.reset_index()
    spain.columns = ['index','Ciudad','Com.Autonoma']

    spain_result = pd.DataFrame(info_product_.groupby('region_code')['pk_partition'].count().sort_values(ascending=False).head(10))
    spain_result.reset_index(inplace=True)
    spain_result = pd.merge(spain_result, spain, left_on='region_code', right_on='index', how='left')

    fig1 = px.bar(spain_result, x='Ciudad', y='pk_partition')
    
    # Not Spain
    abroad_result = pd.DataFrame(info_product_.groupby('country_id')['pk_partition'].count().sort_values(ascending=False).head(11))
    abroad_result.reset_index(inplace=True)
    abroad_result = abroad_result[ abroad_result['country_id'] != 'ES']

    country_match = {}
    for key, value in paises_code.items():
        country_match[key] = value[1]

    abroad_result['Pais'] = abroad_result['country_id'].replace(country_match)
    
    fig2 = px.bar(abroad_result, x='Pais', y='pk_partition')

    fig3 = channel(info_product_)

    return fig1, fig2, fig3
    

def channel(info_product_):
    channel_result = pd.DataFrame(info_product_.groupby('entry_channel')['pk_partition'].count().sort_values(ascending=False).head(10))
    channel_result.reset_index(inplace=True)

    fig = px.bar(channel_result , x='entry_channel', y='pk_partition')

    return fig


def active_userss(dir_path):

    active_clients = obtain_socioproductscommercial(dir_path)
    active_clients = socioproductscommercial.copy(deep=True)
    active_clients['num_products'] = active_clients[ prod ].sum(axis=1)
    active_clients = active_clients[ (active_clients['num_products'] != 0) & (active_clients['active_customer'] != 0) & (active_clients['pk_partition'] == '2019-05-28') ]