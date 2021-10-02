from setuptools import setup
import os, re

def readme():
    with open("README.md") as f:
        return f.read()

def version():
    """
    Return package version as listed in `__version__` in `__init__.py`.
    """
    path = os.path.join("git_substatus", "__init__.py")
    with open(path, "rb") as f:
        init_py = f.read().decode("utf-8")
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

setup(
    name="git-substatus",
    author="Metin Yazici",
    version=version(),
    description="Display the 'git status' in sub-directories",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="git sub status fetch directory folder",
    url="https://github.com/strboul/git-substatus",
    python_requires=">=3.8",
    license="MIT",
    packages=["git_substatus"],
    entry_points = {
        "console_scripts": ["git-substatus=git_substatus.__main__:main"],
    }
)
