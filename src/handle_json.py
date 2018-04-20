import json
import logging
import socket


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