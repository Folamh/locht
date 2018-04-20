import json
import logging
from datetime import datetime
import global_vars
import os
import argparse
import save
import diagram
from record import record


def read_config():
    with open(os.path.join(global_vars.dir_path, global_vars.args.config)) as json_data:
        global_vars.config = json.load(json_data)


def setup_logger():
    log_format = '%(asctime)-15s %(levelname)s: %(message)s'
    logging.basicConfig(format=log_format, level=logging.DEBUG)


def setup_argparse():
    parser = argparse.ArgumentParser(description='Locht')
    parser.add_argument('--config', '-c', action='store', default='configs/config.json')
    parser.add_argument('--profile', '-p', action='store', dest="profile")
    parser.add_argument('--record', '-r', action='store_true')
    parser.add_argument('--test', '-t', action='store_true')
    parser.add_argument('--save', '-s', action='store_true')
    parser.add_argument('--diagram', '-d', action='store_true')
    return parser.parse_args()


def read_profile():
    with open(os.path.join(global_vars.dir_path, global_vars.args.profile)) as json_file:
        global_vars.profile = json.load(json_file)


def generate_filename(prefix):
    date = datetime.strftime(datetime.utcnow(), '%Y-%m-%d-%H-%M-%S-%f')
    profile = global_vars.args.profile.split('/')[-1].split('.')[0]
    return '{}-{}-{}'.format(prefix, profile, date)


if __name__ == '__main__':
    global_vars.dir_path = os.path.dirname(os.path.realpath(__file__))
    global_vars.args = setup_argparse()
    read_config()
    setup_logger()
    read_profile()

    lineage = None
    if global_vars.args.record:
        lineage = record()
        if global_vars.args.save:
            save.save_recording(os.path.join(global_vars.dir_path, 'recordings', generate_filename('recording')),
                                lineage)
        if global_vars.args.diagram:
            diagram.build_graph_from_lineage(os.path.join(global_vars.dir_path, 'graphs',
                                                          generate_filename('recording')), lineage)
    if global_vars.args.test:
        pass
