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


class ActionReturnProfessorOffice(Action):
    def name(self) -> Text:
        return "ActionReturnProfessorOffice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        df = listadoDF()
        professor_name = tracker.get_slot("professor_name").upper()

        if professor_name:
            for index, row in df.iterrows():
                df_name = row['NOMBRE'].upper()
                if "".join(df_name.split()) == "".join(professor_name.split()):
                    professor_group = row['GRUPO']
                    response = f"The professor {professor_name} works at office {row['DESPACHO']}."
                    break
                else:
                    response = f"Sorry, I couldn't find any information about the professor {professor_name}."

        else:
            response = "What professor would you like information about?"
            
        dispatcher.utter_message(response)
        return [SlotSet("professor_name", professor_name)]

class ActionReturnProfessorGroup(Action):    
    def name(self) -> Text:
        return "ActionReturnProfessorGroup"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        df = listadoDF()
        professor_name = tracker.get_slot("professor_name").upper()

        if professor_name:
            for index, row in df.iterrows():
                df_name = row['NOMBRE'].upper()
                if "".join(df_name.split()) == "".join(professor_name.split()):
                    professor_group = row['GRUPO']
                    response = f"The professor {professor_name} pertains to the group: {row['GRUPO']}."
                    break
                else:
                    response = f"Sorry, I couldn't find any information about the professor {professor_name}."

        else:
            response = "What professor would you like information about?"
            
        dispatcher.utter_message(response)
        return [SlotSet("professor_group", professor_group)]

class ActionReturnProfessorOfficeAndGroup(Action):
    def name(self) -> Text:
        return "ActionReturnProfessorOfficeAndGroup"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        df = listadoDF()
        professor_name = tracker.get_slot("professor_name").upper()

        if professor_name:
            for index, row in df.iterrows():
                df_name = row['NOMBRE'].upper()
                if "".join(df_name.split()) == "".join(professor_name.split()):
                    professor_group = row['GRUPO']
                    response = f"The professor {professor_name} works at office {row['DESPACHO']} and pertains to group: {row['GRUPO']}."
                    break
                else:
                    response = f"Sorry, I couldn't find any information about the professor {professor_name}."

        else:
            response = "What professor would you like information about?"
            
        dispatcher.utter_message(response)
        return [SlotSet("professor_group", professor_group)]

class ActionReturnProfessorBuilding(Action):
    def name(self) -> Text:
        return "ActionReturnProfessorBuilding"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        df = listadoDF()
        professor_name = tracker.get_slot("professor_name").upper()

        if professor_name:
            for index, row in df.iterrows():
                df_name = row['NOMBRE'].upper()
                if "".join(df_name.split()) == "".join(professor_name.split()):
                    professor_ = row['EDIFICIO']
                    response = f"The professor {professor_name} works at building: {row['EDIFICIO']}."
                    break
                else:
                    response = f"Sorry, I couldn't find any information about the professor {professor_name}."

        else:
            response = "What professor would you like information about?"
            
        dispatcher.utter_message(response)
        return [SlotSet("professor_name", professor_name)]

class ActionReturnProfessorsOfGroup(Action):
    def name(self) -> Text:
        return "ActionReturnProfessorsOfGroup"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        professor_group = tracker.get_slot("professor_group")
        df = listadoDF()

        professors_of_group = df[df['GRUPO'].str.contains(professor_group, case=False)]['NOMBRE']
        response = f"There are {len(professors_of_group)} professors in the group '{professor_group}': {professors_of_group.tolist()}"
        dispatcher.utter_message(response)

        return []

class ActionReturnOfficeOccupation(Action):
    def name(self) -> Text:
        return "ActionReturnOfficeOccupation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        df = listadoDF()
        professor_office = tracker.get_slot("professor_office").upper()
        professor_name = ""
        
        if professor_office:
            for index, row in df.iterrows():
                df_office = row['DESPACHO'].upper()
                if "".join(df_office.split()) == "".join(professor_office.split()):
                    professor_office = row['DESPACHO']
                    professor_name = row['NOMBRE']
                    break
            
            if professor_name:
                professors_of_office = df[df['DESPACHO']==professor_office]['NOMBRE']
                response = f"There are {len(professors_of_office)} professors in the office '{professor_office}': {professors_of_office.tolist()}"
            else:
                response = f"Sorry, I couldn't find any information about the office {professor_office}."

        else:
            response = "What office would you like information about?"
            
        dispatcher.utter_message(response)
        return [SlotSet("professor_name", professor_name if professor_name else None)]




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
    full_path = "listado.csv"

    df = pd.read_csv(full_path, delimiter=';', encoding='latin-1')
    df.columns = ['NOMBRE', 'GRUPO', 'DESPACHO', 'EDIFICIO']
    df = df.dropna(axis = 0, how = 'all')
    df = df.reset_index(drop=True)
    df['NOMBRE'] = df['NOMBRE'].apply(parse_name)
    return df

