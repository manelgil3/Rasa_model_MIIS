# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

#text=row['GRUPO']

import csv
import os
import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List


class ActionReturnProfessorGroup(Action):

    def name(self) -> Text:
        return "ActionReturnProfessorGroup"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        df = listadoDF()
        professor_name = tracker.get_slot("professor_name").upper()
        print(professor_name, "HOLA")


        for index, row in df.iterrows():
            df_name = row['NOMBRE'].upper()
            if "".join(df_name.split()) == "".join(professor_name.split()):
                print("OK")
                professor_group = row['GRUPO']
                response = f"The professor {professor_name} belongs to {professor_group} ."
                break
            else:
                response = "null"
                professor_group = "null"

        dispatcher.utter_message(response)
        return [SlotSet("professor_group", professor_group)]



class ActionSearchProfessor(Action):
    def name(self):
        return "ActionSearchProfessor"

    def run(self, dispatcher, tracker, domain):
        professor_name = tracker.get_slot("professor_name")
        if professor_name:
            with open('listado.csv', mode='r', encoding='latin-1') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    if row['NOMBRE'] == professor_name:
                        response = f"The professor {professor_name} works at office {row['DESPACHO']}."
                        break
                else:
                    response = f"Sorry, I couldn't find any information about the professor {professor_name}."
        else:
            response = "What professor would you like information about?"

        dispatcher.utter_message(response)
        return [SlotSet("professor_name", professor_name)]
    


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