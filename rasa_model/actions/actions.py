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
from rasa_sdk import Action, Tracker
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
        

        # check if the selected option slot is set
        selected_option = tracker.get_slot("selected_option")
        if selected_option is not None:
            # continue with custom action logic
            dispatcher.utter_message("You selected: {}".format(selected_option))
            # clear the slot value for the selected option
            return [SlotSet("selected_option", None), SlotSet("waiting_for_user_input", False)]
        
        # Get entities from user input
        entities = tracker.latest_message.get('entities')
        if not entities:
            response = "No professor name detected. Please try to repeat the question."
            dispatcher.utter_message(response)
            return
        else:
            professor_name = tracker.get_slot("professor_name").upper()
            for entity in entities:
                if ((entity['entity'] == 'PERSON') and (entity['extractor']=='SpacyEntityExtractor')):
                    professor_name = entity['value'].upper()
        

        professors = utils.detectProfessor(professor_name, listado)
        print("professors")
        print(professors)

        if len(professors)==1:
            professor_name = professors[0]['fullname']

            # Generate response and slot
            for index, row in listado.iterrows():

                listado_fullname = utils.remove_all_extra_spaces(row['fullname'].upper())
                if "".join(listado_fullname.split()) == "".join(professor_name.split()):
                    print("OK")
                    professor_group = row['Group']
                    response = f"The professor {professor_name} belongs to {professor_group} ."
                    break
                else:
                    response = "null"
                    professor_group = "null"

            dispatcher.utter_message(response)
            return [SlotSet("professor_group", professor_group). SlotSet("waiting_for_user_input", False)]

        else:
            response = "I found {} possible professors. Which one are you asking for?".format(len(professors))
            dispatcher.utter_message(response)
            for idx, x in enumerate(professors):
                response = "[{}]{}".format(idx, x['fullname'])
                dispatcher.utter_message(response)
                # set a slot to wait for the user's response
            return [SlotSet("waiting_for_user_input", True), FollowupAction("option_form")]

            # # create button templates for each option
            # buttons = []
            # for x in professors:
            #     payload = "/select_option{\"option\": \"" + x['fullname'] + "\"}"
            #     buttons.append({"title": x['fullname'], "payload": payload})

            # # send a message with the button templates
            # dispatcher.utter_message(response=buttons)


            
        
    
    # def events_for_user(self) -> List[EventType]:
    #     return [SlotSet("waiting_for_user_input", False)]


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
        return "action_ask_option"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(
            text=
        )

        option = tracker.get_slot("option")

        # set the slot value for the selected option
        return [SlotSet("selected_option", option)]
    