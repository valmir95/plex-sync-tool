from enum import Enum, auto


class ComparatorStrategy(Enum):
    COMPARE_WITH_MEDIA_ID_GUID = auto()
    COMPARE_WITH_NAME_AND_YEAR = auto()