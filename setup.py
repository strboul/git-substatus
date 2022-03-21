import subprocess

from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


def get_versions():
    def get_version(variable):
        cmd = ["./get_version.sh", variable]
        run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        return run.stdout.decode("utf-8").strip("\n")

    out = {}
    out["version"] = get_version("__version__")
    out["py_version"] = get_version("__py_version__")
    return out


setup(
    name="git-substatus",
    author="Metin Yazici",
    version=get_versions()["version"],
    description="Display the 'git status' in sub-directories",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="git sub status fetch directory folder",
    url="https://github.com/strboul/git-substatus",
    python_requires=f">={get_versions()['py_version']}",
    license="MIT",
    packages=["git_substatus"],
    entry_points={
        "console_scripts": ["git-substatus=git_substatus.__main__:main"],
    },
)
