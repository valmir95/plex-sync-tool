from enum import Enum


class TVRating(Enum):
    TV_Y = "TV-Y"
    TV_Y7 = "TV-7"
    TV_Y7_FV = "TV-Y7 FV"
    TV_G = "TV-G"
    TV_PG = "TV-PG"
    TV_14 = "TV-14"
    TV_MA = "TV-MA"

    @staticmethod
    def from_str(label):
        try:
            return TVRating[label.replace("-", "_").replace(" ", "_")]
        except:
            return None
