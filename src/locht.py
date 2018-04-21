import json
import logging
from datetime import datetime
import global_vars
import os
import argparse
import save
import diagram
from experiment import experiment
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
    parser.add_argument('--lineage', '-l', action='store', dest="lineage")
    parser.add_argument('--test', '-t', action='store_true')
    parser.add_argument('--save', '-s', action='store_true')
    parser.add_argument('--diagram', '-d', action='store_true')
    parser.add_argument('--instructions', '-i', action='store', dest="instructions")
    return parser.parse_args()


def read_profile():
    if global_vars.args.profile:
        with open(os.path.join(global_vars.dir_path, global_vars.args.profile)) as json_file:
            global_vars.profile = json.load(json_file)


def read_instructions():
    with open(os.path.join(global_vars.dir_path, global_vars.args.instructions)) as json_file:
        return json.load(json_file)


def read_lineage():
    with open(os.path.join(global_vars.dir_path, global_vars.args.lineage)) as json_file:
        return json.load(json_file)


def generate_filename(prefix, subject):
    date = datetime.strftime(datetime.utcnow(), '%Y-%m-%d-%H-%M-%S-%f')
    return '{}-{}-{}'.format(prefix, subject, date)


if __name__ == '__main__':
    global_vars.dir_path = os.path.dirname(os.path.realpath(__file__))
    global_vars.args = setup_argparse()
    read_config()
    setup_logger()
    read_profile()

    lineage = None
    instructions = None
    if global_vars.args.record:
        lineage = record()
        if global_vars.args.save:
            save.save_recording(os.path.join(global_vars.dir_path, 'recordings',
                                             generate_filename('recording', global_vars.args.profile
                                                               .split('/')[-1].split('.')[0])), lineage)
        if global_vars.args.diagram:
            diagram.build_graph_from_lineage(os.path.join(global_vars.dir_path, 'graphs',
                                                          generate_filename('recording', global_vars.args.profile
                                                                            .split('/')[-1].split('.')[0])), lineage)
    if global_vars.args.lineage:
        lineage = read_lineage()
        if global_vars.args.diagram:
            diagram.build_graph_from_lineage(os.path.join(global_vars.dir_path, 'graphs',
                                                          generate_filename('diagram', global_vars.args.lineage
                                                                            .split('/')[-1].split('.')[0])), lineage)

    if global_vars.args.test:
        if global_vars.args.instructions:
            instructions = read_instructions()
            experiment(instructions)
