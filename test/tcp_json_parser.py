import json
import os
import re

dir_path = os.path.dirname(os.path.realpath(__file__))


with open(os.path.join(dir_path, 'samples', 'lineage.txt'), 'r') as file:
    array = file.read().split('}{')
    array[0] = array[0] + '}'
    for index in range(1, len(array) - 1):
        array[index] = '{' + array[index] + '}'
    array[-1] = '{' + array[-1]

    recordings = {}
    for json_string in array:
        json_dict = json.loads(json_string)
        for key in json_dict:
            regex = re.compile(r'(.*?'
                               r')-(.*)-(\d+)')
            if regex.search(key):
                recordings.update(json_dict)
                # print(json_dict)

    steps = []
    for key in recordings:
        for recording in recordings[key]:
            steps.append(recording)
    # print(steps)
    steps.sort(key=lambda json: tuple(map(int, list(json.keys())[0].split('-'))))
    print(steps)
    work_tree = {}
    for index, lineage in enumerate(steps):
        work_tree.update({index: lineage})

    print(work_tree)
