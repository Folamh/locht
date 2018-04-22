def sort_and_enumerate(lineage):
    lineage.sort(key=lambda json: tuple(map(int, list(json.keys())[0].split('-'))))
    temp_lineage = {}
    for index, lineage in enumerate(lineage):
        for key in lineage:
            temp_lineage.update({index: lineage[key]})
    return temp_lineage


def clean_lineage(lineage):
    temp_lineage = {}
    step_counter = 0
    for key, value in lineage.items():
        if value not in temp_lineage.values():
            temp_lineage[str(step_counter)] = value
            step_counter = step_counter + 1
    return temp_lineage
