import os
from collections.abc import Iterator

from git_substatus.utils import list_directories, sort_by_basename


class Directory:
    def __init__(self, path: str, *, include_hidden: bool):
        self._path = path
        self.include_hidden = include_hidden

    @property
    def path(self) -> str:
        return os.path.expanduser(self._path)

    def get_sub_directories(self) -> tuple[str, ...]:
        """
        Get the paths of sub directories (limit: 1) in a given directory.
        """
        if not self.__is_directory:
            raise FileNotFoundError(f"Error: not a directory: '{self._path}'")
        sub_dirs = tuple(self.__sub_directories())
        sub_dirs_sorted = sort_by_basename(sub_dirs)
        return sub_dirs_sorted

    @property
    def __is_directory(self) -> bool:
        return os.path.isdir(self._path)

    def __sub_directories(self) -> Iterator[str]:
        sub_dirs = list_directories(self.path)
        sub_dirs_path = tuple(os.path.join(self.path, sb) for sb in sub_dirs)
        for sdp in sub_dirs_path:
            if self.include_hidden:
                yield sdp
            else:
                if not os.path.basename(sdp).startswith("."):
                    yield sdp
