import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go

pd.options.display.float_format = '{:,.2f}'.format


def read_data(a = None):
  dir_path = '/Users/carlosperezricardo/Documents/data/'

  altas_df = pd.read_csv(dir_path+'altas.csv', encoding='utf-8', index_col=0)
  bajas_df = pd.read_csv(dir_path+'bajas.csv', encoding='utf-8', index_col=0)
  productos_exist_df = pd.read_csv(dir_path+'products_exist.csv', encoding='utf-8', index_col=0)

  return altas_df, bajas_df, productos_exist_df


def tipos_producto(df, products_dict):
  ahorros = df.copy(deep=True)
  financiacion = df.copy(deep=True)
  cuentas = df.copy(deep=True)

  for key, value in products_dict.items():
    if value == 'ahorro e inversión':
      ahorros[key] = df[key]
    else:
      ahorros.drop(columns=key, inplace=True)
    if value == "financiación":
      financiacion[key] = df[key]
    else:
      financiacion.drop(columns=key, inplace=True)
    if value == "cuenta":
      cuentas[key] = df[key]
    else:
      cuentas.drop(columns=key, inplace=True)

  return ahorros, financiacion, cuentas


def obtencion_ingresos(altas_df, products_dict, cost_product):  
  # Obtencion de ingresos
  ingresos_df = altas_df.copy(deep=True)

  for key, value in products_dict.items():
    ingresos_df[key] = ingresos_df[key]*cost_product[value] 

  ahorros_df, financiacion_df, cuentas_df = tipos_producto(ingresos_df, products_dict)

  return ingresos_df, ahorros_df, financiacion_df, cuentas_df 


def fig_resumen_mes(financiacion_df, ahorros_df, cuentas_df):
  resumen_mes = pd.DataFrame( [financiacion_df.sum(axis=1)['2019-05-28'], ahorros_df.sum(axis=1)['2019-05-28'], cuentas_df.sum(axis=1)['2019-05-28']], index=['Financiacion', 'Ahorros', 'Cuentas'], columns=['ingresos'])
  resumen_mes = resumen_mes.reset_index()
  resumen_mes.columns = ['tipo','ingresos']
 
  fig = px.bar(resumen_mes, x="ingresos", y=[1,1,1], color='tipo', orientation='h')

  fig.update_layout(legend=dict(
      orientation="h",
      yanchor="bottom",
      y=1.02,
      xanchor="center",
      x=0.5,
      font=dict(
              family="Courier",
              size=18,
              color="black"
      )
  ))

  fig.update_yaxes(visible=False, showticklabels=False)

  return fig


def alta_baja_total (df, name):
  x = df[1:]
  totales = pd.DataFrame(x.sum(axis='columns')).reset_index()  
  totales.columns = ['pk_partition',name]

  return totales


def fig_altas_bajas(altas_df, bajas_df):
  altas_totales = alta_baja_total (altas_df, 'altas')
  bajas_totales = alta_baja_total (bajas_df, 'bajas')

  fig = go.Figure()
  fig.add_trace(go.Scatter(x=altas_totales["pk_partition"], y=altas_totales["altas"], name='Altas'))
  fig.add_trace(go.Scatter(x=bajas_totales["pk_partition"], y=bajas_totales["bajas"], name='Bajas'))

  if altas_totales.max()['altas'] > bajas_totales.max()['bajas']:
    max_value = altas_totales.max()['altas']
  else:
    max_value = bajas_totales.max()['bajas']
  fig.update_yaxes(range=[0, max_value*1.05])
  #fig.update_layout(#title='Productos: Altas y Bajas',
  #                  yaxis_title='Cantidad de productos')
  fig.update_layout(yaxis_title='Cantidad de productos')

  fig.update_layout(legend=dict(
      orientation="h", yanchor="bottom", y=1.02,
      xanchor="center", x=0.5,
      font=dict(family="Courier",size=14,color="black")
  ))

  return fig


def obtener_ingresos_totales(df):
  totales = pd.DataFrame(df[1:].sum(axis='columns')).reset_index()
  totales.columns = ['pk_partition','ingresos']
  return totales


def fig_ingresos_totales(ingresos_df, ahorros_df, cuenta_df, financiacion_df):
  totales_ingresos = obtener_ingresos_totales(ingresos_df)

  totales_ahorros = obtener_ingresos_totales(ahorros_df)
  totales_financiacion = obtener_ingresos_totales(financiacion_df)
  totales_cuentas = obtener_ingresos_totales(cuenta_df)

  fig = go.Figure()
  fig.add_trace(go.Scatter(x=totales_ingresos['pk_partition'], y=totales_ingresos['ingresos'], name='Total'))

  fig.add_trace(go.Scatter(x=totales_ingresos['pk_partition'], y=totales_ahorros['ingresos'], name='Ahorros'))
  fig.add_trace(go.Scatter(x=totales_ingresos['pk_partition'], y=totales_financiacion['ingresos'], name='Financiacion'))
  fig.add_trace(go.Scatter(x=totales_ingresos['pk_partition'], y=totales_cuentas['ingresos'], name='Cuentas'))

  fig.update_yaxes(range=[0, totales_ingresos.max()['ingresos']*1.05])
  #fig.update_layout(title= 'Evolución de los Ingresos',
  #                  yaxis_title='Ingresos mensuales')
  fig.update_layout(yaxis_title='Ingresos mensuales')

  fig.update_layout(legend=dict(
      orientation="h", yanchor="bottom", y=1.02,
      xanchor="center", x=0.5,
      font=dict(family="Courier",size=14,color="black")
  ))

  return fig


def tipo_producto_totales (df, ahorros, financiacion, cuentas):

  totales = alta_baja_total(df, 'value')

  ahorros_totales = alta_baja_total(ahorros, 'value')
  financiacion_totales = alta_baja_total(financiacion, 'value')
  cuentas_totales = alta_baja_total(cuentas, 'value')

  fig = go.Figure()
  fig.add_trace(go.Scatter(x=totales["pk_partition"], y=totales["value"], name='Totales'))

  fig.add_trace(go.Scatter(x=totales["pk_partition"], y=ahorros_totales["value"], name='Ahorros'))
  fig.add_trace(go.Scatter(x=totales["pk_partition"], y=financiacion_totales["value"], name='Financiación'))
  fig.add_trace(go.Scatter(x=totales["pk_partition"], y=cuentas_totales["value"], name='Cuentas'))

  fig.update_yaxes(range=[0, totales.max()['value']*1.05])
  #fig.update_layout(title='Evolución de altas',
  #                 yaxis_title='Número de altas')

  fig.update_layout(legend=dict(
      orientation="h", yanchor="bottom", y=1.02,
      xanchor="center", x=0.5,
      font=dict(family="Courier",size=14,color="black")
  ))

  return fig


def fig_crecimiento(ingresos_df):
  ingresos_tabla = ingresos_df.sum(axis=1).reset_index()
  ingresos_tabla.columns = ['pk_partition', 'ingresos']
  ingresos_tabla = ingresos_tabla[1:]

  ingresos_tabla['ingresos_old'] = ingresos_tabla['ingresos'].shift(1)

  ingresos_tabla['rate'] = (ingresos_tabla['ingresos'] - ingresos_tabla['ingresos_old'])/ingresos_tabla['ingresos_old']*100
  
  fig = px.area(ingresos_tabla, x="pk_partition", y="rate")

  #fig.update_layout(title= 'Evolución del crecimiento mensual (Ingresos)',
  #                 yaxis_title='Crecimiento mensual')
  fig.update_layout(yaxis_title='Crecimiento mensual')

  return fig, ingresos_tabla


def fig_ingresos_tipo (tipo_ingresos):

  ingresos_totales = obtener_ingresos_totales(tipo_ingresos)
    
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=ingresos_totales['pk_partition'], y=ingresos_totales['ingresos'], name='Totales'))

  for prod in tipo_ingresos.columns:
    ing = tipo_ingresos[1:]
    ing = ing[prod]
    fig.add_trace(go.Scatter(x=ingresos_totales['pk_partition'], y=ing, name=prod))

  #fig.update_layout(title= 'Evolución de los Ingresos ({})'.format(tipo_producto),
  #                  yaxis_title='Ingresos mensuales')  
  fig.update_layout(yaxis_title='Ingresos mensuales')

  fig.update_layout(legend=dict(
      orientation="h", yanchor="bottom", y=-1.02,
      xanchor="center", x=0.5,
      font=dict(family="Courier",size=14,color="black")
  ))


  return fig


def polar_ingresos(ingresos_df):
  totales_ingresos = obtener_ingresos_totales(ingresos_df)
  
  totales_ingresos['pk_partition'] = pd.to_datetime(totales_ingresos['pk_partition'])
  totales_ingresos['month'] = totales_ingresos['pk_partition'].dt.month
  totales_ingresos['year'] = totales_ingresos['pk_partition'].dt.year

  months = {1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}

  totales_ingresos['month_name'] = totales_ingresos['month'].map(months)

  month_map = {'Enero':4,'Febrero':3,'Marzo':2,'Abril':1,'Mayo':12,'Junio':10,'Julio':10,'Agosto':9,'Septiembre':8,'Octubre':7,'Noviembre':6,'Diciembre':5}
  totales_ingresos = totales_ingresos.sort_values('month')

  totales_ingresos['order'] = totales_ingresos['month_name'].map(month_map)
  totales_ingresos = totales_ingresos.sort_values('order')

  df_2019 = totales_ingresos[totales_ingresos['year'] == 2019]
  df_2018 = totales_ingresos[totales_ingresos['year'] == 2018]

  #
  df_2018 = df_2018.append( {'pk_partition':'enero', 'ingresos':np.nan, 'month':1, 'month_name':months[1], 'order':month_map[months[1]]}, ignore_index=True )
  df_2018 = df_2018.sort_values('order')

  fig = go.Figure()
  fig.add_trace(go.Scatterpolar(r=df_2018['ingresos'], theta=df_2018['month_name'], name='2018', mode='markers', marker=dict(size=20)))
  fig.add_trace(go.Scatterpolar(r=df_2019['ingresos'], theta=df_2019['month_name'], name='2019', mode='markers', marker=dict(size=20)))

  fig.update_layout(
      polar = dict(
        radialaxis = dict(
          angle = -90,
          tickangle = -90 # so that tick labels are not upside down
        )
      )
  )

  fig.update_layout(legend=dict(
      orientation="h", yanchor="bottom", y=1.01,
      xanchor="center", x=0.5,
      font=dict(family="Courier",size=14,color="black")
  ))
  
  return fig


def fig_churn_plot(tipo_productos, tipo_altas, tipo_bajas):
  # Global (all)
  churn_all = tipo_productos.copy(deep=True)
  churn_cols = []

  for x in churn_all.columns:
    churn_all['old'] = churn_all[x].shift(1)
    churn_all['altas'] = tipo_altas[x]
    churn_all['bajas'] = tipo_bajas[x]
    name = x+'_rate'
    churn_all[name] = churn_all['bajas']/(churn_all['old'] + churn_all['altas'])*100
    churn_cols.append(name)

  churn_all = churn_all[1:]
  churn_all = churn_all.reset_index()
  #churn_global

  fig = go.Figure()
  for x in churn_cols:
    fig.add_trace(go.Scatter(x=churn_all['pk_partition'], y=churn_all[x], name=x))

  fig.update_layout(legend=dict(
      orientation="h", yanchor="bottom", y=-1.0,
      xanchor="center", x=0.5,
      font=dict(family="Courier",size=14,color="black")
  ))

  return fig


