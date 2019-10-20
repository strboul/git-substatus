
import os
import subprocess
import unittest

class TestSubStatus(unittest.TestCase):

    def test_substatus(self):
        cmd_str = ["python3", "git-substatus.py", os.path.join("tests", "test-project-folder")]
        expected_out = "• \x1b[1m\x1b[4m\x1b[34mprojA\x1b[0m (\x1b[37mmaster\x1b[0m) \x1b[33m1 deleted, 2 modified, 1 new\x1b[0m\n• \x1b[1m\x1b[4m\x1b[34mprojB\x1b[0m (\x1b[37mmaster\x1b[0m) \x1b[3m\x1b[32m<sync>\x1b[0m\n• \x1b[1m\x1b[4m\x1b[34mprojC\x1b[0m (\x1b[37mmaster\x1b[0m) \x1b[33m1 merge conflict\x1b[0m\n• \x1b[1m\x1b[4m\x1b[34mprojD\x1b[0m (\x1b[37mmaster\x1b[0m) \x1b[33m1 new\x1b[0m\n• \x1b[1m\x1b[4m\x1b[34mprojE\x1b[0m (\x1b[37mnew-model-branch\x1b[0m) \x1b[3m\x1b[32m<sync>\x1b[0m\n"
        out = subprocess.check_output(cmd_str).decode()
        self.assertEqual(out, expected_out)

if __name__ == '__main__':
    unittest.main()

