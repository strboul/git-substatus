from tests.base import *

from git_substatus.gitsubstatus import GitSubstatusApplication

class TestRepository(TestBase):

    def test_gitsubstatus(self):
        gitsubstatus = GitSubstatusApplication({
            "path": self.temp_test_dir,
            "fetch": False,
            "dont_ignore_hidden": False,
        })

        self.assertEqual(gitsubstatus.exec(), 0)

    def test_gitsubstatus_with_no_repos(self):
        gitsubstatus = GitSubstatusApplication({
            "path": os.path.join(self.temp_test_dir, "proj-no-git1"),
            "fetch": False,
            "dont_ignore_hidden": False,
        })

        with self.assertRaises(SystemExit) as cm:
            gitsubstatus.exec()

        self.assertEqual(cm.exception.code, 1)

if __name__ == "__main__":
    unittest.main()
