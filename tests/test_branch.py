from tests.base import *

from git_substatus.directory import Directory
from git_substatus.repository import Repository

from git_substatus.branch import Branch

class TestBranch(TestBase):

    def test_get_branch_head(self):
        directory = Directory(self.temp_test_dir, False)
        sub_dirs = directory.get_sub_directories()
        repository = Repository(sub_dirs)
        git_repos = repository.get_git_repository_paths()
        branch = Branch(git_repos)
        branches = branch.get_branch_head()
        self.assertEqual(
            branches,
            ("master", "master", "master", "new-branch", "branchie", "master",)
        )


if __name__ == "__main__":
    unittest.main()
