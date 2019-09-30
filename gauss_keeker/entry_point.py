#!/usr/bin/env python3

import os
import glob
import time
import argparse
import multiprocessing as mp

import yaml
import coloredlogs

from sensor import ChangeSensor
from handler import PredPipeHandler, ConfSyncHandler


# TODO: available to multiprocess
class Keeker:
    def __init__(self, event_type: str, filepath: str, offset_root: str, LOGGER):
        self.target_file = filepath
        self.handler_type = event_type
        self.offset_root = offset_root
        self.LOGGER = LOGGER

    def set_components(self):
        self.sensor = ChangeSensor(self.target_file, self.offset_root, LOGGER) 
        if self.handler_type == 'predpipe':
            self.filter = FilterManager().predpipe
            self.handler = PredPipeHandler(self.filter)
        elif self.handler_type == 'confsync':
            self.filter = FilterManager().confsync
            self.handler = ConfSyncHandler(self.filter)

        # TODO: Set Spooler

    def keek(self):
        is_changed = self.sensor.detect()

        text = None
        next_offset = None
        if is_changed:
            text, next_offset = self.sensor.read()

            self.handler.handle(text) # TODO : implement
            self.sensor.commit(next_offset)

            # TODO; Update result with Spooler

        else:
            time.sleep(60)

    def close(self):
        self.sensor.close()
        self.handler.close()


def work(event_type: str, filepath: str, offset_root: str, LOGGER):
    keeker = Keeker(event_type, filepath, offset_root, LOGGER)
    keeker.set_components()
    retcode = 0

    try:
        while True:
            keeker.keek()
            break

    except KeyboardInterrupt:
        LOGGER.warning("receive SIGINT (probably from Docker)")
        retcode = 3
    except:
        LOGGER.exception("exception caught at the top level")
        retcode = 1
    finally:
        keeker.close()

    exit(retcode)


###########################################
#######       MAIN PROCEDURE      #########
###########################################


log_format = "%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s"
coloredlogs.install(fmt=log_format, milliseconds=True)
LOGGER = coloredlogs.logging.getLogger()

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', default='keeker.yml', help='config yaml file')

args = vars(parser.parse_args())
config_yml = args.get('file')

if not os.path.exists(config_yml):
    msg = "There is no %s file." % config_yml
    LOGGER.error(msg)
    exit(1)

# read yml file and extract information for tracking logs
with open(config_yml) as f:
    conf_dict = yaml.safe_load(f)
    msg = "Found %s file. Loaded." % config_yml
    LOGGER.info(msg)

outputs = conf_dict.get('outputs')
file_output_path = None
for output in outputs:
    if output['type'] == 'file':
        file_output_path = output.get('path')

offset_path = conf_dict.get('offset_path')

if file_output_path is None or offset_path is None:
    LOGGER.error("Not exist 'offset_path' and 'file output path' in yaml file")
    exit(1)

# Make directories to store data
if not os.path.exists(offset_path):
    os.makedirs(offset_path)
if not os.path.exists(file_output_path):
    os.makedirs(file_output_path)

msg = "offset_path: %s\t file_output_path: %s" % (offset_path, file_output_path)
LOGGER.info(msg)

# Make target file pool
inputs = conf_dict.get('inputs')
if len(inputs) == 0:
    LOGGER.error("No inputs, Specify inputs in keeker.yml file")
    exit(1)
    
target_file_pool = []

for inp in inputs:
    temp_paths = []
    for path in inp['paths']:
        temp_paths += glob.glob(path)

    temp_paths = list(set(temp_paths))

    if inp['type'] == 'predpipe':
        temp_paths = [('predpipe', filepath) for filepath in temp_paths]
        target_file_pool += temp_paths

    elif inp['type'] == 'oonfsync':
        temp_paths = [('confsync', filepath) for filepath in temp_paths]
        target_file_pool += temp_paths

workers = []
for target in target_file_pool:
    event_type, filepath = target
    workers.append(mp.Process(target=work, args=(event_type, filepath, offset_path, LOGGER)))

for worker in workers:
    worker.start()
    worker.join()

# TODO: Once develop standalone keeker, if requires to have multiprocess keeker, will develop
# TODO: 1. Recognize changes(sensor)

# TODO: 2. If file changes are catched, call EventHandler

# TODO; 3. Classify event based on specific log-module type

# TODO: 4. Calculate statistics and store result

# TODO; 5. Store result to somewhere (maybe file?)

