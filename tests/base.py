import os
import unittest


class TestBase(unittest.TestCase):
    """
    Common setUp and tearDown for the tests.
    """

    @classmethod
    def setUpClass(cls):
        cls.temp_test_dir = os.path.join("tests", "generated-test-proj-dir")
        # list dir is to check if dir exists
        os.listdir(cls.temp_test_dir)
