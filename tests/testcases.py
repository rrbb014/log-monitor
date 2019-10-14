multi_line_messages = """2020-09-25 16:39:29,888 - ERROR - start_pred.py - 29 - exception caught at the top level pipeline_id:AT0204-fanta-river-delta-lactose40
Traceback (most recent call last):
File "start_pred.py", line 21, in <module>
logger=logger)
File "/usr/local/lib/python3.5/dist-packages/gauss_pipe/entry_point.py", line 68, in start_stream_pred
eof = processor.process()
File "/usr/local/lib/python3.5/dist-packages/gauss_pipe/processor.py", line 67, in process
self._pipeline.predict(self._score_thresholds, self._postproc_params)
File "/usr/lib/python3.5/site-packages/training_framework.egg/training_framework/algorithms/iforest_forest.py", line 283, in predict
if len(score_thresholds) > 0:
TypeError: object of type 'NoneType' has no len()
2019-09-25 16:40:00,741 - INFO - __init__.py - 118 - start logging"""

event_cls_case1 = """2019-09-25 16:39:25,930 - INFO - __init__.py - 118 - start logging
2019-09-25 16:39:25,930 - INFO - start_pred.py - 14 - arguments: ['start_pred.py', '/shared', '/shared/AT0204-fanta-river-delta-lactose40_0.log', '/shared/confAT0204-fanta-river-delta-lactose40.json']
2019-09-25 16:39:25,938 - INFO - kafka_reader.py - 63 - connecting to topic prep_0000000000_d_ip with config {'enable.partition.eof': False, 'bootstrap.servers': 'prep1:9092,prep2:9092,prep3:9092', 'default.topic.config': {'auto.offset.reset': 'earliest'}, 'group.id': 'grp_AT0204-fanta-river-delta-lactose40', 'enable.auto.offset.store': False} pipeline_id:AT0204-fanta-river-delta-lactose40
2019-09-25 16:39:26,185 - INFO - processor.py - 42 - updating processing components with max-latency 120.000000 pipeline_id:AT0204-fanta-river-delta-lactose40
2019-09-25 16:39:29,406 - INFO - kafka_reader.py - 165 - starting reading Kafka stream at time 2019-09-21 00:15:21+00:00 KST pipeline_id:AT0204-fanta-river-delta-lactose40
2019-09-25 16:39:29,407 - INFO - processor.py - 157 - expected-time: 0.10; pushed: 1485; max-lat: 120.000000; now-msg_time: 404648.4 pipeline_id:AT0204-fanta-river-delta-lactose40
2019-09-25 16:39:29,811 - INFO - entry_point.py - 18 - gracefully cleaning up pipeline_id:AT0204-fanta-river-delta-lactose40
2019-09-25 16:39:29,811 - INFO - entry_point.py - 21 - closing reader pipeline_id:AT0204-fanta-river-delta-lactose40
2019-09-25 16:39:29,887 - INFO - entry_point.py - 28 - closing output sink pipeline_id:AT0204-fanta-river-delta-lactose40
2019-09-25 16:39:29,888 - INFO - entry_point.py - 34 - all services are closed. Ready to exit and restart. pipeline_id:AT0204-fanta-river-delta-lactose40
2019-09-25 16:39:29,888 - ERROR - start_pred.py - 29 - exception caught at the top level pipeline_id:AT0204-fanta-river-delta-lactose40 Traceback (most recent call last): File "start_pred.py", line 21, in <module> logger=logger) File "/usr/local/lib/python3.5/dist-packages/gauss_pipe/entry_point.py", line 68, in start_stream_pred eof = processor.process() File "/usr/local/lib/python3.5/dist-packages/gauss_pipe/processor.py", line 67, in process self._pipeline.predict(self._score_thresholds, self._postproc_params) File "/usr/lib/python3.5/site-packages/training_framework.egg/training_framework/algorithms/iforest_forest.py", line 283, in predict if len(score_thresholds) > 0: TypeError: object of type 'NoneType' has no len()"""

emptydata_case1 = """2019-09-16 05:17:07,509 - INFO - processor.py - 128 - empty data pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:11,710 - INFO - processor.py - 128 - empty data pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:15,911 - INFO - processor.py - 128 - empty data pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:20,110 - INFO - processor.py - 128 - empty data pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:24,310 - INFO - processor.py - 128 - empty data pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:28,510 - INFO - processor.py - 128 - empty data pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:32,709 - INFO - processor.py - 128 - empty data pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:36,909 - INFO - processor.py - 128 - empty data pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:41,109 - INFO - processor.py - 128 - empty data pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:45,309 - INFO - processor.py - 128 - empty data pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:49,508 - INFO - processor.py - 128 - empty data pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:53,708 - INFO - processor.py - 128 - empty data pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:54,259 - INFO - hdfs_sink.py - 49 - writing predictions to /aidemo_pred__tmp__/19_09_16_05_17_54_259643-b67.csv pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:54,259 - INFO - client.py - 449 - Writing to '/aidemo_pred__tmp__/19_09_16_05_17_54_259643-b67.csv'. pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:54,316 - INFO - hdfs_sink.py - 54 - moving /aidemo_pred__tmp__/19_09_16_05_17_54_259643-b67.csv to /aidemo_pred/ pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:54,316 - INFO - client.py - 862 - Renaming '/aidemo_pred__tmp__/19_09_16_05_17_54_259643-b67.csv' to '/aidemo_pred/19_09_16_05_17_54_259643-b67.csv'. pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:54,322 - INFO - kafka_reader.py - 192 - comitted partition:offset 11:958 on Kafka pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:54,323 - INFO - zk_load_balancer.py - 32 - publishing speed 1.7149 for pipeline AT0103-four-charlie-winter-july64 pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:54,323 - INFO - zk_load_balancer.py - 47 - creating ephemeral prefixed by /speeds/ephemeral pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:54,324 - INFO - zk_load_balancer.py - 54 - ephemeral /speeds/ephemeralFaZvWuRzQD created pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:54,324 - INFO - zk_load_balancer.py - 60 - speed 1.7149 published for pipeline AT0103-four-charlie-winter-july64 pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:17:58,339 - INFO - processor.py - 128 - empty data pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0
2019-09-16 05:18:02,547 - INFO - processor.py - 128 - empty data pipeline_id:AT0103-four-charlie-winter-july64 elastic:False docker_id:0"""
