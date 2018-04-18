import json
import logging
import socket
import re
import global_vars


def parse_json(json_string):
    logging.debug('Json: {}'.format(json_string))
    string_array = json_string.split('}{')
    if len(string_array) != 1:
        string_array[0] = string_array[0] + '}'
        for index in range(1, len(string_array) - 1):
            string_array[index] = '{' + string_array[index] + '}'
        string_array[-1] = '{' + string_array[-1]
    json_array = []
    for json_string in string_array:
        json_array.append(json.loads(json_string))
    return json_array


def send_json(host, port, json_data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(bytes(json.dumps(json_data), 'utf-8'))

        full_response = ''
        while True:
            response = str(sock.recv(4096), 'utf-8')
            if response:
                full_response = full_response + response
            else:
                break
        sock.close()
        return full_response


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
            raise Exception("Unable to start recording on host: ".format(host))


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
            raise Exception("Unable to reset host: ".format(host))

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
            temp_lineage[step_counter] = value
            step_counter = step_counter + 1
    return temp_lineage


def record():
    start_recording()
    input('Please run transaction. Press enter when complete...')
    lineage = finish_recording()
    lineage = sort_and_enumerate(lineage)
    lineage = clean_lineage(lineage)
    return lineage
