# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

#text=row['GRUPO']

import csv
import os
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionReturnProfessor(Action):

    def name(self) -> Text:
        return "ActionReturnProfessor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open('listado.csv', mode='r', encoding='latin-1') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:
                if row['NOMBRE'] == "LOBO , JORGE":
                    dispatcher.utter_message(text=row['GRUPO'])
                    break

        return []



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



