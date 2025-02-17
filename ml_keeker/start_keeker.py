#!/usr/bin/env python3

import re
import os
import glob
import time
import argparse
import multiprocessing as mp

import yaml
import coloredlogs

from ml_keeker.sensor import ChangeSensor
from ml_keeker.handler import EventHandler
from ml_keeker.rule_filter import FilterManager
from ml_keeker.status import StatusManager
from ml_keeker.reporter import FileStatusReporter


class Keeker:
    def __init__(
            self,
            event_type: str,
            filepath: str,
            offset_root: str,
            status_root: str,
            output_root: str,
            logger):

        self.target_file = filepath
        self.handler_type = event_type
        self.offset_root = offset_root
        self.status_root = status_root
        self.output_root = output_root
        self.object_id = os.path.split(filepath)[1].split(".")[0]
        self.logger = logger

        self.set_components()

    def set_components(self):
        # ChangeSensor
        self.sensor = ChangeSensor(
                filepath=self.target_file,
                offset_root=self.offset_root,
                logger=logger
            ) 

        # EventHandler
        self.filter = FilterManager()[self.handler_type]
        self.handler = EventHandler(
            _filter=self.filter,
            logger=self.logger
        )

        # StatusManager
        _ , filename = os.path.split(self.target_file)
        title, _ = os.path.splitext(filename)

        self.stat_manager = StatusManager(
                store_rootpath=self.status_root,
                name=title,
                logger=self.logger
            )

        # StatusReporter
        self.stat_reporter = FileStatusReporter(
                status_rootpath=self.status_root,
                output_rootpath=self.output_root,
                logger=self.logger
            )

    def keek(self) -> bool:
        is_changed = self.sensor.detect()

        text = None
        next_offset = None
        if is_changed:
            # read line from ChangeSensor
            text, next_offset, eof = self.sensor.read()
            self.sensor.commit(private_offset=next_offset)

            # Classify log event
            data_dict = self.handler.handle(text)
            if event_type == "pred_engine":
                engine_id_pattern = re.compile("engine[0-9]{5}")
                engine_id = engine_id_pattern.findall(self.object_id)[0]
                data_dict["id"] = engine_id

            # Store event status
            stored_switch = self.stat_manager.store(data_dict, eof=eof)
            if stored_switch:
                self.sensor.commit(offset=next_offset)
            

            # TODO: Report status
            #self.stat_reporter.report()

        else:
            self.logger.info("No changes")
            return True
        
        return False


    def close(self):
        self.sensor.close()
        self.handler.close()
        self.stat_manager.close()
        #TODO: self.stat_reporter.close()


def work(
        event_type: str,
        filepath: str,
        offset_root: str,
        status_root: str,
        output_root: str,
        logger):

    keeker = Keeker(
            event_type=event_type,
            filepath=filepath,
            offset_root=offset_root,
            status_root=status_root,
            output_root=output_root,
            logger=logger)

    keeker.set_components()
    retcode = 0

    start_keeking = time.time()
    rest_time = 60 * 10    # 10 min

    try:
        while True:
            if time.time() - start_keeking >= rest_time:
                logger.info("Take a rest")
                time.sleep(60)
                start_keeking = time.time()

            exit_flag = keeker.keek()
            if exit_flag:
                break

    except KeyboardInterrupt:
        logger.warning("receive SIGINT (probably from Docker)")
        retcode = 3
    except:
        logger.exception("exception caught at the top level")
        retcode = 1
    finally:
        keeker.close()

    exit(retcode)


###########################################
#######       MAIN PROCEDURE      #########
###########################################



parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', default='keeker_setting.yml', help='config yaml file')
parser.add_argument('--multi', action='store_true', help="Whether single or multi process")
parser.add_argument('--debug', action='store_true', help='Set logger level as DEBUG')


args = vars(parser.parse_args())
config_yml = args.get('file')
multi = args.get('multi')
debug = args.get('debug')

log_format = "%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s"
if debug:
    coloredlogs.install(level=coloredlogs.logging.DEBUG, fmt=log_format, milliseconds=True)
else:
    coloredlogs.install(fmt=log_format, milliseconds=True)
    
logger = coloredlogs.logging.getLogger()

if not os.path.exists(config_yml):
    msg = "There is no %s file." % config_yml
    logger.error(msg)
    exit(1)

# read yml file and extract information for tracking logs
with open(config_yml) as f:
    conf_dict = yaml.safe_load(f)
    msg = "Found %s file. Loaded." % config_yml
    logger.info(msg)


global_settings = conf_dict.get('global')

if global_settings is None:
    logger.error("Should specify 'global' in keeker.yml")
    exit(1)

offset_path = global_settings.get('offset_path')
status_path = global_settings.get('status_path')
file_output_path = global_settings.get("output_path")

if file_output_path is None or offset_path is None or status_path is None:
    logger.error("Not exist 'offset_path' or 'file output path' or 'status_path' in yaml file")
    exit(1)

# Make directories to store data
if not os.path.exists(offset_path):
    os.makedirs(offset_path)
if not os.path.exists(file_output_path):
    os.makedirs(file_output_path)
if not os.path.exists(status_path):
    os.makedirs(status_path)

msg = "offset_path: %s\t file_output_path: %s\t status_path: %s" % (offset_path, file_output_path, status_path)
logger.info(msg)

# Make target file pool
inputs = conf_dict.get('input')
if len(inputs) == 0:
    logger.error("No input, Specify input(s) in keeker.yml file")
    exit(1)
    
target_file_pool = []

for inp in inputs:
    temp_paths = []
    for path in inp['paths']:
        logger.debug(path)
        temp_paths += glob.glob(path)

    temp_paths = list(set(temp_paths))

    temp_paths = [(inp["type"], filepath) for filepath in temp_paths]
    target_file_pool += temp_paths


if multi:
    # Multi process version keeker 
    logger.info("Multi-process execution")
    workers = []
    for target in target_file_pool:
        event_type, filepath = target
        workers.append(mp.Process(target=work, args=(event_type, filepath, offset_path, status_path, file_output_path, logger)))
        logger.info("worker, %s %s %s %s %s" % (event_type, filepath, offset_path, status_path, file_output_path))

    for worker in workers:
        worker.start()
        worker.join()

else:
    logger.debug("target_file_pool:")
    logger.debug(target_file_pool)
    # Single process version keeker
    logger.info("Single process execution")
    for target in target_file_pool:
        event_type, filepath = target
        work(event_type, filepath, offset_path, status_path, file_output_path, logger)
