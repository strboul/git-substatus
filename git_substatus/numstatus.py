from collections.abc import Callable, Iterator
from typing import TypedDict


class TypeText(TypedDict):
    singular: str
    plural: str


class NumStatus:
    """
    A class to get the number of status changes for some git attributes,
    e.g. stash, worktree etc.
    """

    def __init__(self, repos: tuple[str, ...], txt: TypeText, fun_get_num: Callable):
        self.repos = repos
        self.txt = txt
        self.fun_get_num = fun_get_num

    def get_num(self) -> tuple[str, ...]:
        nums = tuple(self.__num_iterator())
        return nums

    def __num_iterator(self) -> Iterator[str]:
        for repo in self.repos:
            num = self.fun_get_num(repo)
            if len(num) > 0:
                num = self.__num_text(num)
            yield num

    def __num_text(self, num: str) -> str:
        txt = self.txt["plural"] if int(num) > 1 else self.txt["singular"]
        return f"{num} {txt}"
