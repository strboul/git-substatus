import os
import subprocess
import tempfile
import unittest


class TestBase(unittest.TestCase):
    """
    Common setUp and tearDown for the tests.
    """

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.initial_wd = os.getcwd()

        os.chdir(cls.temp_dir.name)

        test_path = os.path.join(cls.initial_wd, "tests", "gen_test_repos.sh")

        # run the shell file silently:
        cmd = test_path + " > /dev/null 2>&1"
        subprocess.check_output(cmd, shell=True)

        cls.temp_test_dir = os.path.join(
            cls.temp_dir.name, "tests", "generated-test-proj-dir"
        )

        os.chdir(cls.temp_test_dir)

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.initial_wd)
        cls.temp_dir.cleanup()
