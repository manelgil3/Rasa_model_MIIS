# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

#text=row['GRUPO']

import csv
import nltk
import numpy as np
import os
import pandas as pd
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from typing import Any, Text, Dict, List, Union
import utils

listado = utils.listadoDF()
professors = []
groups = []

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


class ActionReturnGroupProfessors(Action):
    def name(self):
        return "ActionReturnGroupProfessors"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        group_professors = []
        groups = utils.get_group_from_entity(dispatcher, tracker, listado)
        if not groups: return

        # Generate response and slot
        if len(groups)==1:
            group_name = groups[0]['name']

            listado_filter = listado.loc[listado['Group'] == group_name]
            listado_filter.index = np.arange(1, len(listado_filter) + 1)
            if listado_filter.empty:
                response = "No group detected with name: {}".format(group_name)
                dispatcher.utter_message(response)
                return
            for idx, row in listado_filter.iterrows():
                professor_name = utils.remove_all_extra_spaces(row['fullname'].upper())
                print(professor_name)
                group_professors.append("[{}]{}\n".format(idx, professor_name))

            response = f"The group {group_name} has {len(listado_filter)} professors:\n"
            dispatcher.utter_message(response)
            for p in group_professors:
                dispatcher.utter_message(p)
            return [
                SlotSet("professor_group", group_name), 
                SlotSet("waiting_for_user_input", False),
                SlotSet("GROUP", group_name),
                SlotSet("professors", professor_name),
                #SlotSet('groups', None)
                SlotSet('selected_group', None)
            ]
        else:
            return [SlotSet("waiting_for_user_input", True),SlotSet('groups', groups), FollowupAction("ActionSelectGroup")]
        


        



        # professor_name = tracker.get_slot("professor_name")
        # if professor_name:
        #     with open('listado.csv', mode='r', encoding='latin-1') as f:
        #         reader = csv.DictReader(f, delimiter=';')
        #         for row in reader:
        #             if row['NOMBRE'] == professor_name:
        #                 response = f"The professor {professor_name} works at office {row['DESPACHO']}."
        #                 break
        #         else:
        #             response = f"Sorry, I couldn't find any information about the professor {professor_name}."
        # else:
        #     response = "What professor would you like information about?"

        # dispatcher.utter_message(response)
        # return [SlotSet("professor_name", professor_name)]
    

class ActionSelectProfessor(Action):

    def name(self) -> Text:
        return "ActionSelectProfessor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        professors = tracker.get_slot('professors')
        if not professors: return []
        
        dispatcher.utter_message(
            text="I've found {} possible professors. Which one are you asking for?".format(len(professors)),
            buttons=[{"title":p['fullname'], "payload":'/inform{{"selected_professor":"{}"}}'.format(p['fullname'])} for p in professors]
        )
        return []
    
class ActionSelectGroup(Action):

    def name(self) -> Text:
        return "ActionSelectGroup"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        groups = tracker.get_slot('groups')
        if not groups: return[]

        dispatcher.utter_message(
            text="I've found {} possible groups. Which one are you asking for?".format(len(groups)),
            buttons=[{"title":g['name'], "payload":'/inform{{"selected_group":"{}"}}'.format(g['name'])} for g in groups]
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
    