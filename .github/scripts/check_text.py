import argparse
import difflib
import subprocess


def get_file_lines(filename):
    with open(filename) as file:
        lines = file.readlines()
    return lines


def get_readme_text(lines, start_pattern, end_pattern):
    start_index = lines.index(start_pattern) + 1
    end_index = lines.index(end_pattern)
    sublines = lines[start_index:end_index]
    # remove backticks
    sublines = [line for line in sublines if line != "```\n"]
    text = "".join(sublines)
    return text


def get_command_output(command):
    cmd = command.split(" ")
    out = None
    run = subprocess.run(cmd, stdout=subprocess.PIPE)
    if run.returncode == 0:
        out = run.stdout.decode("utf-8")
        return out
    raise ValueError("could not get the help text")


def check_if_equal(command_output, readme_text):
    equal = command_output == readme_text
    if not equal:
        d1 = command_output.splitlines(keepends=True)
        d2 = readme_text.splitlines(keepends=True)
        print("".join(difflib.ndiff(d1, d2)))
        print("* * *")
        raise ValueError("readme text is not up-to-date")
    print("help output in readme is up-to-date")


def get_cli_args():
    parser = argparse.ArgumentParser(
        description="Check a block of text in a file against an output returned by a command or any other piped output."
    )
    parser.add_argument("--file", required=True, help="file to check the block")
    parser.add_argument("--pattern_start", required=True, help="start pattern")
    parser.add_argument("--pattern_end", required=True, help="end pattern")
    parser.add_argument("--command", required=True, help="command to check the output")
    parsed_args = parser.parse_args()
    # this solution isn't great as it also removes the other unicode characters
    # but so far, I don't have any use case so fine.
    parsed_args.pattern_start = bytes(parsed_args.pattern_start, "utf-8").decode(
        "unicode_escape"
    )
    parsed_args.pattern_end = bytes(parsed_args.pattern_end, "utf-8").decode(
        "unicode_escape"
    )
    return parsed_args


def main():
    args = get_cli_args()
    lines = get_file_lines(args.file)
    readme_text = get_readme_text(lines, args.pattern_start, args.pattern_end)
    command_output = get_command_output(args.command)
    check_if_equal(command_output, readme_text)
    return 0


if __name__ == "__main__":
    main()
