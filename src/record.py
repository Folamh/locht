import logging
import re

import global_vars
from handle_json import send_json, parse_json
from transaction import run_transaction


def start_recording():
    for host in global_vars.profile['hosts']:
        response = send_json(host['host'], 11211, {
            'type': 'RECORD',
            'ports': host['ports']
        })
        response = parse_json(response)
        if response[-1]['type'] == 'RECORD-OK':
            logging.debug('Recording started on {}.'.format(host))
        else:
            raise Exception("Unable to start recording on host: {}".format(host))


def finish_recording():
    lineage = []
    for host in global_vars.profile['hosts']:
        response = send_json(host['host'], 11211, {
            'type': 'RECORD-FINISH'
        })
        response = parse_json(response)
        if response[-1]['type'] == 'FINISH-RECORD-OK':
            logging.debug('Node on {} reset.'.format(host))
        else:
            raise Exception("Unable to finish recording on host: ".format(host))

        for json_data in response:
            for key in json_data:
                regex = re.compile(r'RECORDING')
                if regex.search(key):
                    lineage = lineage + json_data[key]

        response = send_json(host['host'], 11211, {
            'type': 'RESET'
        })
        response = parse_json(response)
        if response[-1]['type'] == 'RESET-OK':
            logging.debug('Node on {} reset.'.format(host))
        else:
            raise Exception("Unable to reset host: {}".format(host))

    return lineage


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


def record():
    logging.info('Recording lineage.')
    start_recording()
    run_transaction(global_vars.profile)
    lineage = finish_recording()
    lineage = sort_and_enumerate(lineage)
    lineage = clean_lineage(lineage)
    logging.info('Recording finished: {}'.format(lineage))
    return lineage
