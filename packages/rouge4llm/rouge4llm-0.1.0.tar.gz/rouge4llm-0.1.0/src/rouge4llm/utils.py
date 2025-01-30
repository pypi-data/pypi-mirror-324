from typing import NewType
from enum import StrEnum

Result = NewType("Result", dict[str, dict[str, float] | float])


class SplitType(StrEnum):
    train = "train"
    val = "validation"
    test = "test"


class AspectType(StrEnum):
    challenge = "challenge"
    approach = "approach"
    outcome = "outcome"
