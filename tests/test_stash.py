from tests.base import *

from git_substatus.directory import Directory
from git_substatus.repository import Repository

from git_substatus.stash import Stash

class TestStash(TestBase):

    def test_get_stash_num(self):
        directory = Directory(self.temp_test_dir, False)
        sub_dirs = directory.get_sub_directories()
        repository = Repository(sub_dirs)
        git_repos = repository.get_git_repository_paths()
        stash = Stash(git_repos)
        stashes = stash.get_num()
        self.assertEqual(stashes, ("", "", "", "", "", "", "2 stashes",))


if __name__ == "__main__":
    unittest.main()
