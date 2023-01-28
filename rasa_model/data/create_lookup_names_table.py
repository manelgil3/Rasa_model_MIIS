import re
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


def parse_name(name):

    """ Source: https://stackoverflow.com/questions/55840700/how-to-parse-a-name-that-is-a-string-in-lastname-firstname-format-into-a-list-i"""
    lst = name.split(',') # this line will split the string into two words

    lst.reverse() # this will reverse the list 
    name = " ".join(lst)
    return name

def main():
    entity = "professor_name"

    text  = 'version: "2.0"\n'
    text += 'nlu:\n'
    text += '  - lookup: {}\n'.format(entity)
    text += '    examples: |\n'

    file_path = "rasa_model/data/listado.csv"
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.replace(' ', '')
    df = df[df['NOMBRE'].notna()]
    df = df.reset_index()  # make sure indexes pair with number of rows

    for index, row in df.iterrows():
        bad_chars = ['','\u008a'] # There is an invisible char here
        regex     = '|'.join(bad_chars)
        professor_name = parse_name(row['NOMBRE'])
        new_line  = re.sub(regex, '', professor_name.strip())#.encode('utf-8').decode('utf-8')
        text += '      - ' + new_line + '\n'

    with open("rasa_model/data/" + entity + '.yml', 'w', encoding='utf-8') as f:
        f.write(text)

if __name__ == "__main__":
    main()
