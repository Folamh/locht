import json


def save_json(filename, json_data):

    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)
