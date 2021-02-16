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


def df_nulls(df):
    pass


def vector(value=None):
    return ['2018-01-28','2018-02-28','2018-03-28','2018-04-28','2018-05-28','2018-06-28','2018-07-28','2018-08-28','2018-09-28','2018-10-28','2018-11-28','2018-12-28','2019-01-28','2019-02-28','2019-03-28','2019-04-28','2019-05-28']
