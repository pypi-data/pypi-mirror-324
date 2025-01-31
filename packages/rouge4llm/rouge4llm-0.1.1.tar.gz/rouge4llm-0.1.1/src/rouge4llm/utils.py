from typing import NewType
from enum import StrEnum

Result = NewType("Result", dict[str, dict[str, float] | float])


class SplitType(StrEnum):
    train = "train"
    val = "validation"
    test = "test"

    @classmethod
    def parse_arg(cls, arg: str | None) -> "SplitType | None":
        if arg is None:
            return None
        else:
            return cls[arg]


class AspectType(StrEnum):
    challenge = "challenge"
    approach = "approach"
    outcome = "outcome"

    @classmethod
    def parse_arg(cls, arg: str | None) -> "AspectType | None":
        if arg is None:
            return None
        else:
            return cls[arg]


class DatasetType(StrEnum):
    scitldr = "scitldr"
    aclsum = "aclsum"

    @classmethod
    def parse_arg(cls, arg: str | None) -> "DatasetType | None":
        if arg is None:
            return None
        else:
            return cls[arg]
