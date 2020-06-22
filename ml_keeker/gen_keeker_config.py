#!/usr/bin/env python3

import os
import time
import shutil
import argparse
import logging 
import yaml

from kazoo.client import KazooClient


def get_kafka_location(zk_host) -> str:
    """ Return Kafka server hosts using zookeeper client """
    client = KazooClient(zk_host)
    client.start()
    
    value, stat = client.get("/gauss/conf/kafka/bootstrap/servers")
    return value.decode("utf8")


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s"
try:
    import coloredlogs
    coloredlogs.install(fmt=LOG_FORMAT)
except ImportError:
    pass

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
LOGGER = logging.getLogger(__name__)

PARSER = argparse.ArgumentParser()
PARSER.add_argument("-p", "--path", default="/shared", help="keeker root path")
PARSER.add_argument("--no-trainer",action="store_true", help="Disable tracing trainer logs")
PARSER.add_argument("--no-engine",action="store_true", help="Disable tracing engine logs")
PARSER.add_argument("--no-kafka",action="store_true", help="Disable sending message to Kafka")
PARSER.add_argument("--zk", help="zookeeper host:ip group, prep1:2181,prep2:2181")
PARSER.add_argument("--kafka-topic", help="Audit log topic name")

args = vars(PARSER.parse_args())

config = {}

BINDING_VOLUME_PATH = args.get("path")
disable_trainer = args.get("no_trainer")
disable_engine = args.get("no_engine")
disable_kafka = args.get("no_kafka")
zk_host = args.get("zk", "localhost:2181")
kafka_topic = args.get("kafka_topic")

if disable_kafka:
    kafka_server = None
    kafka_topic = None

else:
    kafka_server = get_kafka_location(zk_host)
    if kafka_topic is None:
        raise ValueError("Kafka topic required. Use --kafka-topic option")


LOGGER.info("=========================")
LOGGER.info("===      CONFIGS      ===")
LOGGER.info("-------------------------")
LOGGER.info("- SHARED PATH: %s" % BINDING_VOLUME_PATH)
LOGGER.info("- Enable Trainer: {}".format(not disable_trainer))
LOGGER.info("- Enable Engine: {}".format(not disable_engine))
LOGGER.info("- Enable Ouput Kafka: {}".format(not disable_kafka))
LOGGER.info("- Zookeeper host: {}".format(zk_host))
LOGGER.info("- Kafka bootstrap server: {}".format(kafka_server))
LOGGER.info("- Kafka topic name: %s" % kafka_topic)

# backup 
if os.path.exists("keeker_setting.yml"):
    output = "keeker_setting_%s.yml" % time.strftime("%m-%d_%H.%M")
    shutil.copyfile("keeker_setting.yml", output)
    LOGGER.info("Replace keeker_setting.yml to {}".format(output)) 

# Global path
config["global"] = {}
config["global"]["offset_path"] = os.path.join(BINDING_VOLUME_PATH, "offsets")
config["global"]["status_path"] = os.path.join(BINDING_VOLUME_PATH, "status")
config["global"]["output_path"] = os.path.join(BINDING_VOLUME_PATH, "outputs")

# Input path
input_list = []

if not disable_engine:
    input_list.append(
        dict(
           type="pred_engine",
           paths=[os.path.join(BINDING_VOLUME_PATH, "engine*.log")]
        )
    )
    LOGGER.info("Prediction engine config added")

if not disable_trainer:
    input_list.append(
        dict(
            type="trainer",
            paths=[os.path.join(BINDING_VOLUME_PATH, "trainer.log")]
        )
    )
    LOGGER.info("Trainer config added")

config["input"] = input_list

# Output path
output_list = []
if not disable_kafka:
    output_list.append(
        dict(
            type="kafka",
            topic="topic_for_audit"
        )
    )
    LOGGER.info("Kafka output config added")

config["output"] = output_list

with open("keeker_setting.yml", "w", encoding="utf8") as f:
    yaml.safe_dump(config, f)

LOGGER.info("Creation configuration file is done")
