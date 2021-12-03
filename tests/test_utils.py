from git_substatus.utils import *
from tests.base import *


class TestFancyText(unittest.TestCase):
    def test_without_styles(self):
        ft = fancy_text("Grass", "green")
        self.assertEqual(ft, "\x1b[32mGrass\x1b[0m")

    def test_with_styles(self):
        ft = fancy_text("Apple", "red", styles=("bold", "underline"))
        self.assertEqual(ft, "\x1b[1m\x1b[4m\x1b[31mApple\x1b[0m")

    def test_missing_input(self):
        with self.assertRaisesRegex(
            TypeError, "missing 1 required positional argument: 'color'"
        ):
            fancy_text("abc")


class TestFlatten(unittest.TestCase):
    def test_flatten_list(self):
        out = list(flatten(["a", "b", [1, "z"], ["y"]]))
        self.assertEqual(out, ["a", "b", 1, "z", "y"])


if __name__ == "__main__":
    unittest.main()
