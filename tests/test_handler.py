import os
import shutil
import coloredlogs
import unittest

from gauss_keeker.common import RegexRepository
from gauss_keeker.filter import FilterManager
from gauss_keeker.handler import PredPipeHandler

class TestPredPipeHandler(unittest.TestCase):
    def setUp(self):
        # TODO
        
        fm = FilterManager()
        self.handler = PredPipeHandler(fm.predpipe)
        
        pass


    def test_classify(self):
        # For predpipe logs
        texts = """start logging
        argument ['a', 'b', 'c', 'd']

        """
        self.handler(
        pass

    def tearDown(self):
        # TODO
        pass

if __name__ == "__main__":
    ret = unittest.main()
    if len(ret.result.errors + ret.result.failure) > 0:
        exit(1)
