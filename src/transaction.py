import logging
import subprocess

import global_vars


def run_transaction(json={}):
    command = json.get('transaction', None)

    if command:
        try:
            process = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
            output, err = process.communicate(timeout=json.get('timeout', global_vars.config['timeout']))
            logging.info('Transaction complete.')
            return process
        except subprocess.TimeoutExpired:
            logging.warning('Transaction timeout occurred failed experiment')
    else:
        input('Please run transaction. Press enter when complete...')
    return None