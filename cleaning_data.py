from datetime import datetime as dt
import pandas as pd
import numpy as np

def clean_commercial_activity(df_all, partitions):
    df = df_all[ df_all['pk_partition'] == partitions[-1]]
    
    # Categorias 'entry_channel' y 'segment'
    df['entry_channel'] = df['entry_channel'].fillna('Sin Asignar')
    df['segment'] = df['segment'].fillna('Sin Asignar')
    #df = df[ (df['entry_channel'] != 'Sin Asignar') & (df['segment'] != 'Sin Asignar') ]

    df['entry_channel'] = df['entry_channel'].astype('category')
    df['segment'] = df['segment'].astype('category')

    # Fechas erroneas
    wrong_dates = {'2015-02-29': '2015-02-28', '2019-02-29':'2019-02-28'}
    df['entry_date'] = df['entry_date'].replace(wrong_dates)
    df['pk_partition'] = df['pk_partition'].replace(wrong_dates)

    return df


def clean_products(df_all, partitions):
    df = df_all[ df_all['pk_partition'] == partitions[-1]]

    boolean_cols = ["payroll","pension_plan","short_term_deposit", "loans", "mortgage", "funds", "securities", "long_term_deposit", "em_account_pp", "credit_card", "payroll_account", "emc_account", "debit_card", "em_account_p", "em_acount"]

    for x in boolean_cols:
        df[x] = df[x].astype(bool)

    # Fechas erroneas
    wrong_dates = {'2015-02-29': '2015-02-28', '2019-02-29':'2019-02-28'}
    df['pk_partition'] = df['pk_partition'].replace(wrong_dates)

    return df


def clean_sociodemographic(df_all, partitions):
    df = df_all[ df_all['pk_partition'] == partitions[-1]]

    # Fechas erroneas
    wrong_dates = {'2015-02-29': '2015-02-28', '2019-02-29':'2019-02-28'}
    df['pk_partition'] = df['pk_partition'].replace(wrong_dates)

    return df


def df_description(df):
    """ df_description: returns a briefly description of the variables in a dataframe
        inputs: 
            - df : dataframe
        outputs:
            - None (prints information on the terminal)
    """
    print(df.head())

    print('\n\n Dataframe info: \n')
    print(df.info())

    print('\n\n Dataframe description: ')
    print(df.describe(include='all'))  
    
    return None



