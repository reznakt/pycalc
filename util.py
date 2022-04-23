import sys
from dataclasses import dataclass


def frozendataclass(*args, **kwargs):  # type: ignore
    return dataclass(*args, **kwargs, frozen=True)  # type: ignore


class recursionlimit:
    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.old_limit: int

    def __enter__(self) -> None:
        self.old_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(self.limit)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        sys.setrecursionlimit(self.old_limit)
