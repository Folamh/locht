import logging
from time import sleep
import re

import global_vars
from handle_json import send_json, parse_json
from lineage import sort_and_enumerate, clean_lineage
from transaction import run_transaction


def send_instructions(instructions):
    for host in instructions['hosts']:
        full_response = ''
        for instruction in host['steps']:
            instruction.update({"experiment": global_vars.current_experiment})
            response = send_json(host['host'], 11211, instruction)
            full_response = full_response + response
        full_response = parse_json(full_response)
        if full_response[-1]['type'] == 'INSTRUCTIONS-OK':
            logging.debug('Instructions sent to {}.'.format(host))
        else:
            raise Exception("Unable to send instructions to host: {}".format(host))


def start_experiment(instructions):
    for host in instructions['hosts']:
        response = send_json(host['host'], 11211, {
            "type": "START",
            "experiment": global_vars.current_experiment
        })
        response = parse_json(response)
        if response[-1]['type'] == 'START-OK':
            logging.debug('Experiment started on {}.'.format(host))
        else:
            raise Exception("Unable to start experiment on host: {}".format(host))


def finish_experiment(instructions):
    lineage = []
    for host in instructions['hosts']:
        response = send_json(host['host'], 11211, {
            "type": "FINISH"
        })
        response = parse_json(response)
        if response[-1]['type'] == 'FINISH-EXPERIMENT-OK':
            logging.debug('Experiment finished on {}.'.format(host))
        else:
            raise Exception("Unable to finish experiment on host: {}".format(host))

        for json_data in response:
            for key in json_data:
                regex = re.compile(r'EXPERIMENT-{}'.format(global_vars.current_experiment))
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


def experiment(instructions):
    logging.info('Starting experiment.')
    send_instructions(instructions)
    start_experiment(instructions)
    process = run_transaction(instructions)
    if process:
        if process.returncode == 0:
            global_vars.experiment_results.append({str(global_vars.current_experiment): 'Success'})
        else:
            global_vars.experiment_results.append({str(global_vars.current_experiment): 'Fail'})
    else:
        global_vars.experiment_results.append({str(global_vars.current_experiment): 'Fail'})
    lineage = finish_experiment(instructions)
    lineage = sort_and_enumerate(lineage)
    lineage = clean_lineage(lineage)
    logging.info('Experiment finished: {}'.format(lineage))
    return lineage
