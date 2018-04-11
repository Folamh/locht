import json
import socket
import re
import global_vars


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
    print(global_vars.profile)
    for host in global_vars.profile['hosts']:
        response = send_json(host['host'], 11211, {
            'type': 'RECORD',
            'ports': host['ports']
        })

    input('Please run transaction. Press enter when complete...')

    for host in global_vars.profile['hosts']:
        response = send_json(host['host'], 11211, {
            'type': 'RECORD-FINISH'
        })
        print(response)

        array = response.split('}{')
        array[0] = array[0] + '}'
        for index in range(1, len(array) - 1):
            array[index] = '{' + array[index] + '}'
        array[-1] = '{' + array[-1]

        recordings = {}
        for json_string in array:
            json_dict = json.loads(json_string)
            for key in json_dict:
                regex = re.compile(r'(.*?)-(.*)-(\d+)')
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
