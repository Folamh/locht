import json
import os
from datetime import datetime
import global_vars


def save_recording(lineage):
    date = datetime.strftime(datetime.utcnow(), '%Y-%m-%d-%H-%M-%S-%f')
    profile = global_vars.args.profile.split('/')[-1].split('.')[0]
    with open(os.path.join(global_vars.dir_path, 'recording-{}-{}'.format(profile, date)), 'w') as file:
        json.dump(lineage, file)
