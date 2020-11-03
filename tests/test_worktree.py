from tests.base import *

from git_substatus.directory import Directory
from git_substatus.repository import Repository

from git_substatus.worktree import Worktree

class TestWorktree(TestBase):

    def test_have_worktree(self):
        directory = Directory(self.temp_test_dir, False)
        sub_dirs = directory.get_sub_directories()
        repository = Repository(sub_dirs)
        git_repos = repository.get_git_repository_paths()
        worktree = Worktree(git_repos)
        have_worktrees = worktree.have_worktree()
        self.assertEqual(
            have_worktrees,
            (False, False, False, False, True, True, False, )
        )


if __name__ == "__main__":
    unittest.main()
