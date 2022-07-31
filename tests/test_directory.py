import os
import unittest

from git_substatus.directory import Directory

from .base import TestBase


class TestDirectory(TestBase):
    def test_sub_dirs_ignore_hidden(self):
        directory = Directory(self.temp_test_dir, include_hidden=False)
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
        directory = Directory(self.temp_test_dir, include_hidden=True)
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
        path = os.path.join(self.temp_test_dir, "proj-no-git1")
        directory = Directory(path, include_hidden=True)
        self.assertEqual(directory.get_sub_directories(), ())

    def test_path_exist_but_not_directory(self):
        path = os.path.join(self.temp_test_dir, "file1")
        directory = Directory(path, include_hidden=True)
        with self.assertRaises(FileNotFoundError):
            directory.get_sub_directories()


if __name__ == "__main__":
    unittest.main()
