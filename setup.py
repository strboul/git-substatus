import subprocess

from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


def get_version(variable):
    cmd = ["./scripts/get_version.sh", variable]
    run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return run.stdout.decode("utf-8").strip("\n")


setup(
    name="git-substatus",
    author="Metin Yazici",
    version=get_version("__version__"),
    description="Display the 'git status' in sub-directories",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="git sub status fetch directory folder",
    url="https://github.com/strboul/git-substatus",
    python_requires=f">={get_version('__py_version__')}",
    license="MIT",
    packages=["git_substatus"],
    entry_points={
        "console_scripts": ["git-substatus=git_substatus.__main__:main"],
    },
    # Trove classifiers: https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        f"Programming Language :: Python :: {get_version('__py_version__')}",
    ],
)
