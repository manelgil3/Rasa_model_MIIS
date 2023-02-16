import os
import pandas as pd

def parse_name(name):

    """ Source: https://stackoverflow.com/questions/55840700/how-to-parse-a-name-that-is-a-string-in-lastname-firstname-format-into-a-list-i"""
    lst = name.split(',') # this line will split the string into two words

    lst.reverse() # this will reverse the list 
    name = " ".join(lst)
    return name

def listadoDF():
    """
    Returns a pandas dataframe with listado.csv data parsed in 4 columns:
    'NOMBRE' --> name of the professor with format NAME SURNAME(S)
    'GRUPO' --> group where professor belongs
    'DESPACHO' --> office number of the professor with format Integer
    'EDIFICIO' --> building where office belongs with format Edifici La Nau
    """
    absolute_path = os.path.dirname(__file__)
    relative_path = "../data/listado.csv"
    full_path = os.path.join(absolute_path, relative_path)

    df = pd.read_csv(full_path)
    df.columns = ['NOMBRE', 'GRUPO', 'DESPACHO', 'EDIFICIO']
    df = df.dropna(axis = 0, how = 'all')
    df = df.reset_index(drop=True)
    df['NOMBRE'] = df['NOMBRE'].apply(parse_name)
    return df