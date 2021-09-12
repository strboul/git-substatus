from git_substatus.base import *


def exit_program(message: str):
    """
    Sends SIGHUP 1 signal and exits the program.
    """
    raise SystemExit(fancy_text(message, "red"))


def list_directories(path: str) -> List[str]:
    """
    List only directories in a path.
    """
    return next(os.walk(path))[1]


def flatten(lst: Union[List[Any], Tuple[Any, ...]]) -> Iterator[Any]:
    """
    Flatten a nested list or tuple.

    Examples:
    list(flatten(["a", "b", [1, "z"]]))
    """
    for l in lst:
        if isinstance(l, (list, tuple)):
            yield from flatten(l)
        else:
            yield l


def sort_by_basename(arr: Tuple[str, ...]) -> Tuple[str, ...]:
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


def fancy_text(text: str, color: str, styles: Optional[Tuple[str, ...]] = None) -> str:
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
        exit_program("git is not found")


def run_git_command(path: str, what: List[str]) -> str:
    """
    Run a git command in a path.

    :param path str: path to run the git command.
    :param what List[str]: which command(s) to run.

    Details:
    -C <path> comes from that as if git was started in <path> instead
    of the current working directory.
    """
    cmd = list(flatten(["git", "-C", os.path.expanduser(path), what]))
    run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if run.returncode is not 0:
        return ""
    out = run.stdout.decode("utf-8")
    return out


def display_table(cols):
    def get_max_char_width(x: Tuple[str, ...]) -> int:
        return max(map(len, x))

    def nchar_format(x: str, max_char: int) -> str:
        fmt_txt = "{:" + str(max_char) + "}"
        return fmt_txt.format(x)

    def pad_chars(char):
        max_char_width = get_max_char_width(char)
        return tuple(map(lambda x: nchar_format(x, max_char_width), char))

    def get_padded_cols(cols):
        return tuple(map(pad_chars, cols))

    padded_cols = get_padded_cols(cols)

    def print_cols(padded_cols, row_prefix="\u2022"):
        len_rows = len(padded_cols[0])
        len_cols = len(padded_cols)
        for i in range(len_rows):
            row = tuple(zip(*padded_cols))[i]
            fmt_txt = row_prefix + (" {}  " * len_cols).rstrip()
            print(fmt_txt.format(*row))
        return None

    print_cols(padded_cols)
