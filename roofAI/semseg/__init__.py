from enum import Enum, auto


class Profile(Enum):
    FULL = auto()
    QUICK = auto()
    VALIDATION = auto()

    @property
    def data_count(self):
        return {
            Profile.FULL: -1,
            Profile.QUICK: 20,
            Profile.VALIDATION: 1,
        }[self]

    @property
    def epoch_count(self):
        return {
            Profile.FULL: 40,
            Profile.QUICK: 10,
            Profile.VALIDATION: 1,
        }[self]
