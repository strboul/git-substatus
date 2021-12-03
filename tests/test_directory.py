from git_substatus.directory import Directory
from tests.base import *


class TestDirectory(TestBase):
    def test_sub_dirs_ignore_hidden(self):
        directory = Directory(self.temp_test_dir, False)
        sub_dirs = directory.get_sub_directories()
        self.assertEqual(
            tuple(map(os.path.basename, sub_dirs)),
            (
                "proj-no-git1",
                "projA",
                "projB",
                "projC",
                "projD",
                "projE",
                "projE-worktree",
                "projF",
            ),
        )

    def test_sub_dirs_include_hidden(self):
        directory = Directory(self.temp_test_dir, True)
        sub_dirs = directory.get_sub_directories()
        self.assertEqual(
            tuple(map(os.path.basename, sub_dirs)),
            (
                ".proj-no-git2",
                ".projB-remote",
                ".projB-user1",
                "proj-no-git1",
                "projA",
                "projB",
                "projC",
                "projD",
                "projE",
                "projE-worktree",
                "projF",
            ),
        )

    def test_sub_dirs_empty_dir(self):
        pat = os.path.join(self.temp_test_dir, "proj-no-git1")
        directory = Directory(pat, True)
        self.assertEqual(directory.get_sub_directories(), ())

    def test_path_type(self):
        with self.assertRaises(TypeError):
            Directory(1, True)


if __name__ == "__main__":
    unittest.main()
