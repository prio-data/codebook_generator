import pandas as pd
import re
import json
import os

def md2df(file_path):
    with open(file_path, 'r') as f:
        markdown_text = f.read()
    
    data_dict = {}
    current_variable_id = None
    current_column = None
    human_name = None
    variable_id_next = False

    for idx, line in enumerate(markdown_text.splitlines()):
        if line.startswith("# "):
            human_name = line[2:].strip()
        elif line.startswith("## Variable ID"):
            variable_id_next = True
        elif variable_id_next:
            current_variable_id = line.strip()
            data_dict[current_variable_id] = {"Human Name": human_name}
            variable_id_next = False
        elif line.startswith("## "):
            current_column = line[3:].strip()
        elif current_variable_id and current_column:
            if current_column in data_dict[current_variable_id]:
                data_dict[current_variable_id][current_column] += f"\n{line.strip()}"
            else:
                data_dict[current_variable_id][current_column] = line.strip()

    df = pd.DataFrame(data_dict).transpose()
    df.index.name = "Variable ID"

    df = df.applymap(lambda x: x.rstrip('\n') if isinstance(x, str) else x)

    return df

        
def df2json(df, file_name, save_path):

    json_data = df.to_json(orient='index')
    os.makedirs(save_path, exist_ok=True)
    with open(os.path.join(save_path, file_name), 'w') as json_file:
        json_file.write(json_data)

