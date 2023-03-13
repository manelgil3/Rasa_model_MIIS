# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

#text=row['GRUPO']

import csv
import nltk
import os
import pandas as pd
from typing import Dict, Text, Any, List, Union
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from typing import Any, Text, Dict, List
import utils

listado = utils.listadoDF()
professors = []

class ActionReturnProfessorGroup(Action):

    def name(self) -> Text:
        return "ActionReturnProfessorGroup"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
        professors = utils.get_professor_from_entity(dispatcher, tracker, listado)
        if not professors: return

        if len(professors)==1:
            professor_name = professors[0]['fullname']

            # Generate response and slot
            for index, row in listado.iterrows():

                listado_fullname = utils.remove_all_extra_spaces(row['fullname'].upper())
                if "".join(listado_fullname.split()) == "".join(professor_name.split()):
                    professor_group = row['Group']
                    response = f"The professor {professor_name} belongs to {professor_group} ."
                    break
                else:
                    response = "null"
                    professor_group = "null"

            dispatcher.utter_message(response)
            return [
                SlotSet("professor_group", professor_group), 
                SlotSet("waiting_for_user_input", False),
                SlotSet("PERSON", professor_name),
                SlotSet("professor_name", professor_name),
                # SlotSet('professors', None)
                SlotSet('selected_professor', None)
            ]
        else:
            return [SlotSet("waiting_for_user_input", True),SlotSet('professors', professors), FollowupAction("ActionSelectProfessor")]


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
    

class ActionSelectOption(Action):

    def name(self) -> Text:
        return "ActionSelectProfessor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        professors = tracker.get_slot('professors')
        
        dispatcher.utter_message(
            text="I've found {} possible professors. Which one are you asking for?".format(len(professors)),
            buttons=[{"title":p['fullname'], "payload":'/inform{{"selected_professor":"{}"}}'.format(p['fullname'])} for p in professors]
        )
        return []
    
# class ValidateOptionForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_option_form"
    
#     def validate_selected_option(
#             self,
#             slot_value: Any,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         select_option = tracker.latest_message.get('text')
        
#         return [SlotSet('selected_option', select_option), FollowupAction("ActionReturnProfessorGroup")]
    