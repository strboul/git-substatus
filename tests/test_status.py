import unittest

from git_substatus.directory import Directory
from git_substatus.repository import Repository
from git_substatus.status import Status

from .base import TestBase


class TestStatus(TestBase):
    def test_get_status(self):
        directory = Directory(self.temp_test_dir, include_hidden=False)
        sub_dirs = directory.get_sub_directories()
        repository = Repository(sub_dirs)
        git_repos = repository.get_git_repository_paths()
        status = Status(git_repos)
        statuses = status.get_status()
        self.assertEqual(
            statuses,
            (
                "1 deleted, 1 modified, 1 untracked",
                "1 untracked & ahead 2, behind 1",
                "1 unmerged",
                "1 untracked",
                "<sync>",
                "<sync>",
                "1 deleted, 1 renamed",
            ),
        )


if __name__ == "__main__":
    unittest.main()
