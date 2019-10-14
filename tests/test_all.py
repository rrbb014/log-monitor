import os
import shutil
import yaml
import coloredlogs
import unittest

from datetime import datetime

from gauss_keeker.common import RegexRepository
from gauss_keeker.rule_filter import FilterManager
from gauss_keeker.handler import PredPipeHandler
from gauss_keeker.sensor import ChangeSensor
from gauss_keeker.status import StatusManager

import testcases

def gen_testcase_file(test_rootpath, name, messages) -> str:
    filepath = os.path.join(test_rootpath, '%s.log' % name)
    with open(filepath,'w', encoding='UTF-8') as f:
        f.write(messages)

    return filepath


class TestGaussKeeker(unittest.TestCase):
    def setUp(self):
        log_format = "%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s"
        coloredlogs.install(level='DEBUG', fmt=log_format)
        self.logger = coloredlogs.logging.getLogger()
        self.logger.info('start logging')
        
        self.regex_repo = RegexRepository()
        self._test_rootpath = '/home/rrbb/code/tmp/test'
        self._offset_path = os.path.join(self._test_rootpath, 'test_keeker', 'offsets')
        self._status_path = os.path.join(self._test_rootpath, 'test_keeker', 'status')

        os.makedirs(self._test_rootpath, exist_ok=True)
        self.logger.debug("make dir %s" % self._test_rootpath)
        os.makedirs(self._offset_path, exist_ok=True)
        self.logger.debug("make dir %s" % self._offset_path)

        os.makedirs(self._status_path, exist_ok=True)
        self.logger.debug("make dir %s" % self._status_path)

        fm = FilterManager()
        self.handler = PredPipeHandler(fm.predpipe, logger=self.logger)

        # Generate testcases
        self.sensor_multiline_case1 = gen_testcase_file(self._test_rootpath, 'multiline', testcases.multi_line_messages)

        self.emptydata_case1 = gen_testcase_file(self._test_rootpath, 'emptydata_case1', testcases.emptydata_case1)
        self.event_cls_case1 = gen_testcase_file(self._test_rootpath, 'event_cls_case1', testcases.event_cls_case1)

    def test_sensor_multi_line(self):
        self.logger.info("TEST_SENSOR_MULTILINE")
        sensor = ChangeSensor(
                filepath=self.sensor_multiline_case1,
                offset_root=self._offset_path,
                logger=self.logger
            )    
        text, next_offset = sensor.read()
        self.logger.debug(text)
        sensor.commit(next_offset)
        next_text, next_offset = sensor.read()

        exception_flag = False
        self.logger.debug(next_text)

        if not self.regex_repo.check_matched(text, self.regex_repo.log_format):
            self.logger.info('text: %s' % text)
            exception_flag = True
            
        if not self.regex_repo.check_matched(next_text, self.regex_repo.log_format):
            self.logger.info('next_text: %s' % next_text)
            exception_flag = True

        if exception_flag:
            raise 

        sensor.close()

    def test_event_classification(self):
        # For predpipe logs
        # TODO: texts
        self.logger.info("TEST_EVENT_CLASSIFICATION")
        with open(self.event_cls_case1) as f:
            texts = f.readlines()

        event_labels = []
        for text in texts:
            label = self.handler.handle(text).get('event_label')
            self.logger.debug("text: "+text)
            self.logger.debug("label: "+label)
            event_labels.append(label)
            
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

    def test_status_emptydata(self):
        self.logger.info("TEST_STATUS_EMPTYDATA")
        name = 'test_emptydata'
        status_manager = StatusManager(
                store_rootpath=self._status_path,
                name=name,
                logger=self.logger
            )

        with open(self.emptydata_case1) as f:
            texts = f.readlines()
        
        for idx, text in enumerate(texts):
            event_dict = self.handler.handle(text)
            if idx == len(texts)-1:
                status_manager.store(eof=True, **event_dict)
            else:
                status_manager.store(**event_dict)

        stat_file = os.path.join(self._status_path, name) + '.status'
        with open(stat_file) as f:
            stat_dict = yaml.safe_load(f)

        self.logger.info(stat_dict)
        begin_empty_data = stat_dict.get("begin_empty_data")
        end_empty_data = stat_dict.get("end_empty_data")

        datetime_fmt = "%Y-%m-%d %H:%M:%S,%f"
        if begin_obj and end_obj:
            begin_obj = datetime.strptime(begin_empty_data, datetime_fmt)
            end_obj = datetime.strptime(end_empty_data, datetime_fmt)
        else:
            raise
        
        assert end_obj - begin_obj == \
                datetime.strptime("2019-09-16 05:17:58,339", datetime_fmt) \
                - datetime.strptime("2019-09-16 05:18:02,547", datetime_fmt)

    



    def tearDown(self):
        # Delete multiline file
        shutil.rmtree(self._test_rootpath)
        self.logger.info("Remove test directories")


if __name__ == "__main__":
    ret = unittest.main()
    if len(ret.result.errors + ret.result.failure) > 0:
        exit(1)
