import os
import shutil
import coloredlogs
import unittest

from gauss_keeker.common import RegexRepository
from gauss_keeker.sensor import ChangeSensor

class TestChangeSensor(unittest.TestCase):
    def setUp(self):
        log_format = "%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s"
        coloredlogs.install(level='DEBUG', fmt=log_format)
        self.logger = coloredlogs.logging.getLogger()
        self.logger.info('start logging')
        self.regex_repo = RegexRepository()
        self._test_rootpath = '/home/rrbb/code/tmp'
        self._offset_path = os.path.join(self._test_rootpath, 'test_keeker', 'offsets')
        os.makedirs(self._test_rootpath, exist_ok=True)
        self.logger.debug("make dir %s" % self._test_rootpath)

        # Generate temporal test log files
        
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

        self._multiline_file = os.path.join(self._test_rootpath, 'multiline.log')
        with open(self._multiline_file,'w', encoding='UTF-8') as f:
            f.write(multi_line_messages)

        self.logger.debug("Write file %s" % self._multiline_file)

    def test_detect_multi_line_messages(self):
        sensor = ChangeSensor(
                filepath=self._multiline_file,
                offset_root=self._offset_path,
                LOGGER=self.logger
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

    def tearDown(self):
        shutil.rmtree(self._offset_path)
        self.logger.info("Remove offset directories")

        os.remove(self._multiline_file)
        self.logger.info('Remove test-multiline file')

if __name__ == "__main__":
    ret = unittest.main()
    if len(ret.result.errors+rt.result.failures) > 0:
        exit(1)
