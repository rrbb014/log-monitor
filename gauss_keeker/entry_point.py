#!/usr/bin/env python3

import os
import glob
import yaml
import coloredlogs

# TODO: Synchronize log format with gauss modules
coloredlogs.install()
LOGGER = coloredlogs.logging.getLogger()

# read yml file and extract information for tracking logs
with open('keeker.yml') as f:
    conf_dict = yaml.safe_load(f)

outputs = conf_dict.get('outputs')
file_output_path = None
for output in outputs:
    if output['type'] == 'file':
        file_output_path = output.get('path')

offset_path = conf_dict.get('offset_path')

if file_output_path is None or offset_path is None:
    LOGGER.error("Not exist 'offset_path' and 'file output path' in yaml file")
    exit(1)

os.makedirs(offset_path, exist_ok=True)
os.makedirs(file_output_path, exist_ok=True)

# TODO: control agent
inputs = conf_dict.get('inputs')
if len(inputs) == 0:
    LOGGER.error("No inputs, Specify inputs in keeker.yml file")
    exit(1)
    
predpipe_log_type = []
confsync_log_type = []

for inp in inputs:
    temp_paths = []
    for path in inp['paths']:
        temp_paths += glob.glob(path)

    temp_paths = list(set(temp_paths))

    if inp['type'] == 'predpipe':
        predpipe_log_type += temp_paths

    elif inp['type'] == 'oonfsync':
        confsync_log_type += temp_paths


# TODO: 1. Recognize changes(sensor)

# TODO: 2. If file change exists, call EventHandler

# TODO; 3. Classify event based on specific log-module type

# TODO: 4. Calculate statistics and store result

# TODO; 5. Store result to somewhere (maybe file?)

