
import os
import subprocess
import unittest
import textwrap


TEST_GENERATOR_SCRIPT = os.path.join("tests", "generate-test.sh")
TEST_FOLDER = os.path.join("tests", "test-project-folder")


def generate_test_folders():
    """
    Generate the test folders (if necessary)
    """
    if not os.path.isdir(TEST_FOLDER):
        msg = f"""
        The test project folders are not found.
        Generating the file \"{TEST_GENERATOR_SCRIPT}\"
        """
        lines = "-" * 45
        print(lines + textwrap.dedent(msg) + lines + "\n")
        subprocess.call(
            TEST_GENERATOR_SCRIPT,
            stdout=subprocess.PIPE
        )
    return None


class TestSubStatus(unittest.TestCase):

    def __make_command(self, path):
        command = "python3"
        file = "git-substatus.py"
        return [command, file, path]


    def no_sub_git_directories_found(self):
        cmd = self.__make_command(os.path.join(TEST_FOLDER, "proj-no-git1"))
        result = subprocess.run(cmd)
        self.assertEqual(result.returncode, 1)


    def test_project_folder(self):
        cmd = self.__make_command(TEST_FOLDER)
        result = subprocess.check_output(cmd)
        decoded = result.decode(encoding="UTF-8")
        pieces = decoded.strip().split("\n")
        # asciify the character output:
        for p in range(len(pieces)):
            pieces[p] = ascii(pieces[p])

        # test the output line by line:
        self.assertEqual(
            pieces[0],
            "'directory: <tests/test-project-folder>'"
        )
        self.assertEqual(
            pieces[1],
            "'\\u2022 \\x1b[1m\\x1b[4m\\x1b[34mprojA\\x1b[0m [\\x1b[37mmaster\\x1b[0m] \\x1b[33m1 deleted, 2 modified, 1 new\\x1b[0m'"
        )
        self.assertEqual(
            pieces[2],
            "'\\u2022 \\x1b[1m\\x1b[4m\\x1b[34mprojB\\x1b[0m [\\x1b[37mmaster\\x1b[0m] \\x1b[3m\\x1b[32m<sync>\\x1b[0m'"
        )
        self.assertEqual(
            pieces[3],
            "'\\u2022 \\x1b[1m\\x1b[4m\\x1b[34mprojC\\x1b[0m [\\x1b[37mmaster\\x1b[0m] \\x1b[33m1 merge conflict\\x1b[0m'"
        )
        self.assertEqual(
            pieces[4],
            "'\\u2022 \\x1b[1m\\x1b[4m\\x1b[34mprojD\\x1b[0m [\\x1b[37mNone\\x1b[0m] \\x1b[33m1 new\\x1b[0m'"
        )
        self.assertEqual(
            pieces[5],
            "'\\u2022 \\x1b[1m\\x1b[4m\\x1b[34mprojE\\x1b[0m [\\x1b[37mnew-model-branch\\x1b[0m] \\x1b[3m\\x1b[32m<sync>\\x1b[0m'"
        )


if __name__ == '__main__':
    generate_test_folders()
    unittest.main()

