from enum import Enum, auto

chip_width = 480
chip_height = 384


class Profile(Enum):
    FULL = auto()
    DECENT = auto()
    QUICK = auto()
    DEBUG = auto()
    VALIDATION = auto()

    @property
    def data_count(self):
        return {
            Profile.FULL: -1,
            Profile.DECENT: 40,
            Profile.QUICK: 20,
            Profile.DEBUG: 2,
            Profile.VALIDATION: 1,
        }[self]

    @property
    def epoch_count(self):
        return {
            Profile.FULL: 40,
            Profile.DECENT: 10,
            Profile.QUICK: 5,
            Profile.DEBUG: 3,
            Profile.VALIDATION: 1,
        }[self]
