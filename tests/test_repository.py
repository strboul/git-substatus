from git_substatus.directory import Directory
from git_substatus.repository import Repository
from tests.base import *


class TestRepository(TestBase):
    def test_get_git_repositories(self):
        directory = Directory(self.temp_test_dir, False)
        sub_dirs = directory.get_sub_directories()
        repository = Repository(sub_dirs)
        git_repos = repository.get_git_repository_paths()
        self.assertEqual(
            tuple(map(os.path.basename, git_repos)),
            (
                "projA",
                "projB",
                "projC",
                "projD",
                "projE",
                "projE-worktree",
                "projF",
            ),
        )

    def test_get_git_repositories_include_hidden(self):
        directory = Directory(self.temp_test_dir, True)
        sub_dirs = directory.get_sub_directories()
        repository = Repository(sub_dirs)
        git_repos = repository.get_git_repository_paths()
        self.assertEqual(
            tuple(map(os.path.basename, git_repos)),
            (
                ".projB-user1",
                "projA",
                "projB",
                "projC",
                "projD",
                "projE",
                "projE-worktree",
                "projF",
            ),
        )

    def test_get_repo_names(self):
        directory = Directory(self.temp_test_dir, False)
        sub_dirs = directory.get_sub_directories()
        repository = Repository(sub_dirs)
        repo_names = repository.get_repo_names()
        self.assertEqual(
            repo_names,
            (
                "projA",
                "projB",
                "projC",
                "projD",
                "projE",
                "projE-worktree",
                "projF",
            ),
        )


if __name__ == "__main__":
    unittest.main()
