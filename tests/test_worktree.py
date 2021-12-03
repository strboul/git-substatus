from git_substatus.directory import Directory
from git_substatus.repository import Repository
from git_substatus.worktree import Worktree
from tests.base import *


class TestWorktree(TestBase):
    def test_get_worktree_num(self):
        directory = Directory(self.temp_test_dir, False)
        sub_dirs = directory.get_sub_directories()
        repository = Repository(sub_dirs)
        git_repos = repository.get_git_repository_paths()
        worktree = Worktree(git_repos)
        worktrees = worktree.get_num()
        self.assertEqual(
            worktrees,
            (
                "",
                "",
                "",
                "",
                "1 worktree",
                "1 worktree",
                "",
            ),
        )


if __name__ == "__main__":
    unittest.main()
