from enum import Enum


class MovieRating(Enum):
    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"

    @staticmethod
    def from_str(label):
        try:
            return MovieRating[label.replace("-", "_")]
        except:
            return None