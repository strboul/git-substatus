import os
import subprocess
from collections.abc import Iterator
from typing import Any


def list_directories(path: str) -> list[str]:
    """
    List only directories in a path.
    """
    return next(os.walk(path))[1]


def flatten(items: list[Any] | tuple[Any, ...]) -> Iterator[Any]:
    """
    Flatten a nested list or tuple.

    Examples:
    list(flatten(["a", "b", [1, "z"]]))
    """
    for item in items:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item


def sort_by_basename(arr: tuple[str, ...]) -> tuple[str, ...]:
    """
    Sort a tuple containing paths by the basename.

    Examples:
    paths = ("abc/z", "def/a")
    sort_by_basename(paths)
    """
    sorted_arr = tuple(
        sorted(arr, key=lambda a: os.path.splitext(os.path.basename(a))[0])
    )
    return sorted_arr


def fancy_text(text: str, color: str, styles: tuple[str, ...] | None = None) -> str:
    """
    Prints string with ANSI colors on terminal.
    """

    ansi_codes = {
        "parameters": {
            "reset": "0",
            "bold": "1",
            "italic": "3",
            "underline": "4",
        },
        "colors": {
            "black": "30",
            "red": "31",
            "green": "32",
            "yellow": "33",
            "blue": "34",
            "magenta": "35",
            "cyan": "36",
            "white": "37",
            "gray": "90",
        },
    }

    # wrap escape characters:
    for section in ansi_codes:
        ansi_codes[section] = dict(
            zip(
                ansi_codes[section].keys(),
                map(lambda x: f"\033[{x}m", ansi_codes[section].values()),
            )
        )

    if styles is not None:
        text_styles = "".join([ansi_codes["parameters"][style] for style in styles])
    else:
        text_styles = ""

    text = "{styles}{color}{text}{reset}".format(
        styles=text_styles,
        color=ansi_codes["colors"][color],
        text=text,
        reset=ansi_codes["parameters"]["reset"],
    )
    return text


def check_git_installed():
    """
    Checks if git is installed on the system. Exits the program if it is not
    installed.
    """
    import shutil

    cmd = shutil.which("git")
    if cmd is None:
        raise SystemError("Error: git is not found")


def run_git_command(path: str, what: list[str]) -> dict:
    """
    Run a git command in a path.

    :param path str: path to run the git command.
    :param what List[str]: which command(s) to run.

    Details:
    -C <path> comes from that as if git was started in <path> instead
    of the current working directory.
    """
    cmd = list(flatten(["git", "-C", os.path.expanduser(path), what]))
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    res = {"status": False, "output": ""}
    res["status"] = True if proc.returncode == 0 else False
    res["output"] = proc.stdout.decode("utf-8")
    return res


def display_table(cols):
    # get highest character length from each column
    max_length = []
    for col in cols:
        highest = len(max(col, key=len))
        max_length.append(highest)

    rows = zip(*cols)

    for row in rows:
        print("\u2022", end=" ")
        for i, _ in enumerate(row):
            value = row[i]
            max_len = max_length[i]
            fmt_value = value.ljust(max_len)
            print(fmt_value, end="  ")
        print("")
