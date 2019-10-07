import os
import shutil
import coloredlogs
import unittest

from gauss_keeker.common import RegexRepository
from gauss_keeker.filter import FilterManager
from gauss_keeker.handler import PredPipeHandler

class TestPredPipeHandler(unittest.TestCase):
    def setUp(self):
        log_format = "%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s"
        coloredlogs.install(level='DEBUG', fmt=log_format)
        self.logger = coloredlogs.logging.getLogger()
        self.logger.info('start logging')
        
        fm = FilterManager()
        self.handler = PredPipeHandler(fm.predpipe, logger=self.logger)
        

    def test_classify(self):
        # For predpipe logs
        texts = """2019-09-25 16:39:25,930 - INFO - __init__.py - 118 - start logging
2019-09-25 16:39:25,930 - INFO - start_pred.py - 14 - arguments: ['start_pred.py', '/shared', '/shared/AT0204-fanta-river-delta-lactose40_0.log', '/shared/confAT0204-fanta-river-delta-lactose40.json']
2019-09-25 16:39:25,938 - INFO - kafka_reader.py - 63 - connecting to topic prep_0000000000_d_ip with config {'enable.partition.eof': False, 'bootstrap.servers': 'prep1:9092,prep2:9092,prep3:9092', 'default.topic.config': {'auto.offset.reset': 'earliest'}, 'group.id': 'grp_AT0204-fanta-river-delta-lactose40', 'enable.auto.offset.store': False} pipeline_id:AT0204-fanta-river-delta-lactose40
2019-09-25 16:39:26,185 - INFO - processor.py - 42 - updating processing components with max-latency 120.000000 pipeline_id:AT0204-fanta-river-delta-lactose40
2019-09-25 16:39:29,406 - INFO - kafka_reader.py - 165 - starting reading Kafka stream at time 2019-09-21 00:15:21+00:00 KST pipeline_id:AT0204-fanta-river-delta-lactose40
2019-09-25 16:39:29,407 - INFO - processor.py - 157 - expected-time: 0.10; pushed: 1485; max-lat: 120.000000; now-msg_time: 404648.4 pipeline_id:AT0204-fanta-river-delta-lactose40
2019-09-25 16:39:29,811 - INFO - entry_point.py - 18 - gracefully cleaning up pipeline_id:AT0204-fanta-river-delta-lactose40
2019-09-25 16:39:29,811 - INFO - entry_point.py - 21 - closing reader pipeline_id:AT0204-fanta-river-delta-lactose40
2019-09-25 16:39:29,887 - INFO - entry_point.py - 28 - closing output sink pipeline_id:AT0204-fanta-river-delta-lactose40
2019-09-25 16:39:29,888 - INFO - entry_point.py - 34 - all services are closed. Ready to exit and restart. pipeline_id:AT0204-fanta-river-delta-lactose40
2019-09-25 16:39:29,888 - ERROR - start_pred.py - 29 - exception caught at the top level pipeline_id:AT0204-fanta-river-delta-lactose40 Traceback (most recent call last): File "start_pred.py", line 21, in <module> logger=logger) File "/usr/local/lib/python3.5/dist-packages/gauss_pipe/entry_point.py", line 68, in start_stream_pred eof = processor.process() File "/usr/local/lib/python3.5/dist-packages/gauss_pipe/processor.py", line 67, in process self._pipeline.predict(self._score_thresholds, self._postproc_params) File "/usr/lib/python3.5/site-packages/training_framework.egg/training_framework/algorithms/iforest_forest.py", line 283, in predict if len(score_thresholds) > 0: TypeError: object of type 'NoneType' has no len()""".split('\n')

        event_labels = [self.handler.handle(text) for text in texts]
        answers = [
                'INIT-start_logger',
                'INIT-print_args',
                'INIT-connect_kafka',
                'INIT-update_component',
                'READ-start_read_msg',
                'READ-expect_time',
                'CLOSE-clean_up',
                'CLOSE-close_reader',
                'CLOSE-close_sink',
                'RESTART',
                'ERROR'
            ]

        if not answers == event_labels:
            self.logger.debug("event_labels: %s" % " ".join(event_labels))
            self.logger.debug("answers: %s" % " ".join(answers))
            unmatched_label = []
            for idx, el in enumerate(zip(event_labels, answers)):
                clf, ans = el
                if clf != ans:
                    unmatched_label.append((clf, texts[idx], ans))
            msg = """"""
            for clf, text, ans in unmatched_label:
                msg += "classified: %s\tanswer: %s\tmessage:%s\n" % (clf, ans, text)

            self.logger.error(msg)
            assert answers == event_labels

    def tearDown(self):
        # TODO
        pass

if __name__ == "__main__":
    ret = unittest.main()
    if len(ret.result.errors + ret.result.failure) > 0:
        exit(1)
