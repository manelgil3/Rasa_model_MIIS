from collections import Counter
import os
import pandas as pd
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
import nltk

def parse_name(name):

    """ Source: https://stackoverflow.com/questions/55840700/how-to-parse-a-name-that-is-a-string-in-lastname-firstname-format-into-a-list-i"""
    lst = name.split(',') # this line will split the string into two words

    lst.reverse() # this will reverse the list 
    name = " ".join(lst)
    return name

def listadoDF():
    """
    Returns a pandas dataframe with listado.csv data parsed in 4 columns:
    'Name1' --> name of the professor with format NAME SURNAME(S)
    'Group' --> Group where professor belongs
    'Office' --> Office number of the professor with format Integer
    'Building' --> Building where office belongs with format Edifici La Nau
    """
    absolute_path = os.path.dirname(__file__)
    relative_path = "../data/listado.csv"
    full_path = os.path.join(absolute_path, relative_path)

    df = pd.read_csv(full_path)
    df.columns = ['fullname', 'Group', 'Office', 'Building']
    df = df.dropna(axis = 0, how = 'all')
    df = df.reset_index(drop=True)
    df['fullname'] = df['fullname'].apply(parse_name)
    df['fullname'] = df['fullname'].apply(remove_leading_space)
    df = split_fullname(df)
    df = df.dropna(axis = 0, how = 'all')
    df = df.reset_index(drop=True)
    return df

def remove_leading_space(s):
    return s.lstrip()
def remove_all_extra_spaces(string):
    return " ".join(string.split())

def split_fullname(df):
    df['Name1'] = ""
    df['Name2'] = ""
    df['Surname1'] = ""
    df['Surname2'] = ""
    for index, row in df.iterrows():
        name_length = len(row['fullname'].split())
        if name_length == 4:
            row[['Name1', 'Name2', 'Surname1', 'Surname2']] = row['fullname'].split()
        elif name_length == 3:
            row[['Name1', 'Surname1', 'Surname2']] = row['fullname'].split()
        elif name_length == 2:
            row[['Name1','Surname1']] = row['fullname'].split()
    return df


def detectProfessor(professor_name:str, listado:pd.DataFrame):
    name = professor_name.split()
    print("detecting professor for name --> " + professor_name)
    professors = []
    for name_part in name:
        for index, row in listado.iterrows():
            name_splitted = [row['Name1'],row['Name2'],row['Surname1'],row['Surname2']]
            if len("".join(name_splitted).replace(" ", ""))==0:continue
            min_dist = min([nltk.edit_distance(name_part, x) for x in name_splitted])
            professor = {
                "fullname":remove_all_extra_spaces(" ".join(name_splitted)),
                "dist": min_dist
            }

            if not professors:
                professors.append(professor)
            elif professors[0]['dist'] > min_dist:
                professors.clear()
                professors.append(professor)
            elif professors[0]['dist'] == min_dist:
                professors.append(professor)
            elif professors[0]['dist'] < min_dist:
                continue

    # Get a Counter object of the professors in the list
    counter = Counter(map(str, professors))
    max_count = max(counter.values())
    print(counter)
    if max_count == 1:
        return professors
    else:
        professors = [dict(eval(key)) for key, count in counter.items() if count == max_count]
        return professors
    
def get_professor_from_entity(dispatcher:CollectingDispatcher, tracker: Tracker, listado:pd.DataFrame):
    # Get entities from user input
        entities = tracker.latest_message.get('entities')
        print(entities)
        if not entities:
            response = "No professor name detected. Please try to repeat the question. Remember names go with capital letters."
            dispatcher.utter_message(response)
            return []
        else:
            professor_name = tracker.get_slot("professor_name").upper()
            selected_professor = tracker.get_slot("selected_professor")
            for entity in entities:
                if ((entity['entity'] == 'PERSON') and (entity['extractor']=='SpacyEntityExtractor')):
                    professor_name = entity['value'].upper()
            if selected_professor is not None:
                professor_name = selected_professor.upper()
        
        professors = detectProfessor(professor_name, listado)
        return professors
