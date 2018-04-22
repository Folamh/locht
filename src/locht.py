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
    parser.add_argument('-c', '--config', action='store', default='configs/config.json',
                        help='change default config. Default configs/config.json.')
    parser.add_argument('-r', '--record', action='store_true',
                        help='record lineage.')
    parser.add_argument('-p', '--profile', action='store', dest="profile",
                        help='profile which to record from.')
    parser.add_argument('-s', '--save', action='store_true',
                        help='save the lineage recorded.')
    parser.add_argument('-l', '--lineage', action='store', dest="lineage",
                        help='pass in a saved lineage.')
    parser.add_argument('-d', '--diagram', action='store_true',
                        help='create a diagram from a lineage.')
    parser.add_argument('-t', '--test', action='store_true',
                        help='test against the system.')
    parser.add_argument('-i', '--instructions', action='store', dest="instructions",
                        help='pass instructions to test the system against.')
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
            save.save_json(os.path.join(global_vars.dir_path, 'recordings',
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
            experiment_lineage = experiment(instructions)
            if global_vars.args.diagram:
                diagram.build_graph_from_lineage(os.path.join(
                    global_vars.dir_path, 'graphs',generate_filename(
                        'experiment', global_vars.args.instructions.split('/')[-1].split('.')[0])), experiment_lineage)
            if global_vars.args.save:
                experiment_lineage.update({'results': global_vars.experiment_results})
                save.save_json(os.path.join(global_vars.dir_path, 'experiments',
                                            generate_filename('experiment', global_vars.args.instructions.split('/')[-1]
                                                              .split('.')[0])), experiment_lineage)
