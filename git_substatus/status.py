from git_substatus.base import *

from git_substatus.utils import run_git_command


class StatusDetails:

    path: str

    @classmethod
    def get_status_details(cls, path: str) -> List[str]:
        cls.path = path

        details_text = cls.__get_details_text()

        details_arr = list(filter(None, details_text.split("\n")))
        details_arr = list(map(lambda da: da.strip(), details_arr))

        return details_arr

    @classmethod
    def __get_details_text(cls) -> str:
        cmd = run_git_command(cls.path, ["status", "-sb"])
        return cmd


class StatusChanges:

    status_details: List[str]
    status_codes: Tuple[str, ...]
    status_count: Dict[str, int]
    mapped_status_count: Dict[str, int]
    status_changes_txt: str

    @classmethod
    def get_status_changes(cls, status_details: List[str]) -> str:

        cls.status_details = status_details

        cls.status_codes = cls.__get_status_codes()
        cls.status_count = cls.__get_status_count()
        cls.mapped_status_count = cls.__get_mapped_status_count()
        cls.status_changes_txt = cls.__get_status_changes_txt()

        return cls.status_changes_txt

    @classmethod
    def __get_status_codes(cls) -> Tuple[str, ...]:
        statuses = cls.status_details[1:]
        codes = tuple(map(lambda l: l.strip().partition(" ")[0], statuses))
        return codes

    @classmethod
    def __get_mapped_status_count(cls) -> Dict[str, int]:
        """
        All status short format codes
        Reference: <https://git-scm.com/docs/git-status>

        X          Y     Meaning
        -------------------------------------------------
                 [AMD]   not updated
        M        [ MD]   updated in index
        A        [ MD]   added to index
        D                deleted from index
        R        [ MD]   renamed in index
        C        [ MD]   copied in index
        [MARC]           index and work tree matches
        [ MARC]     M    work tree changed since index
        [ MARC]     D    deleted in work tree
        [ D]        R    renamed in work tree
        [ D]        C    copied in work tree
        -------------------------------------------------
        D           D    unmerged, both deleted
        A           U    unmerged, added by us
        U           D    unmerged, deleted by them
        U           A    unmerged, added by them
        D           U    unmerged, deleted by us
        A           A    unmerged, both added
        U           U    unmerged, both modified
        -------------------------------------------------
        ?           ?    untracked
        !           !    ignored
        -------------------------------------------------
        """
        # TODO complete them
        status_details = {
            "??": "untracked",
            "?": "untracked",
            "M": "modified",
            "MM": "modified",
            "A": "added",
            "AD": "added to index",
            "AM": "added to index",
            "D": "deleted",
            "R": "renamed",
            "RM": "renamed",
            "UU": "unmerged",
        }

        def status_count_gen():
            for k, v in cls.status_count.items():

                if not k in status_details.keys():
                    raise KeyError(f'Unknown status mapping: "{k}"')

                mapped_count = (status_details.get(k), v)
                yield mapped_count

        return dict(status_count_gen())

    @classmethod
    def __get_status_count(cls) -> Dict[str, int]:
        from collections import Counter

        count_codes = Counter(cls.status_codes)
        return count_codes

    @classmethod
    def __get_status_changes_txt(cls) -> str:
        txt_arr = [f"{v} {k}" for k, v in cls.mapped_status_count.items()]
        # 'natural sort' the array:
        txt_sorted = sorted(txt_arr, key=lambda s: int(s.split(" ")[0]), reverse=True)
        txt = ", ".join(txt_sorted)
        return txt


class StatusAheadBehind:

    status_details: List[str]

    @classmethod
    def get_ahead_behind(cls, status_details: List[str]) -> str:

        cls.status_details = status_details

        status = cls.status_details[0]
        ab_detail = status.split("[")[1].split("]")[0] if "[" in status else ""
        return ab_detail


class Status:
    def __init__(self, repos: Tuple[str, ...]):
        self.repos = repos

    def get_status(self) -> Tuple[str, ...]:
        """
        Main method to get the git status from the given directories.
        """
        git_status = tuple(self.__get_statuses())
        return git_status

    def __get_statuses(self):
        for repo in self.repos:
            status = self.__get_git_status(repo)
            yield status

    def __get_git_status(self, path: str) -> str:

        self.status_details = StatusDetails.get_status_details(path)

        if self.__is_status_clean():
            return "<sync>"

        self.status_changes = StatusChanges.get_status_changes(self.status_details)
        self.ahead_behind = StatusAheadBehind.get_ahead_behind(self.status_details)

        status_list = [self.status_changes, self.ahead_behind]

        out = " & ".join(filter(None, status_list))

        return out

    def __is_status_clean(self) -> bool:
        """
        Checks if working tree contains modifications which have not yet been
        committed to the current branch.
        """
        if len(self.status_details) > 1:
            return False
        # check for the updates in ahead-behind part
        btw_brackets = self.status_details[0].split("[")
        if len(btw_brackets) > 1:
            return False
        return True
