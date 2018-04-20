import json


def save_recording(filename, lineage):

    with open(filename, 'w') as file:
        json.dump(lineage, file, indent=4)
