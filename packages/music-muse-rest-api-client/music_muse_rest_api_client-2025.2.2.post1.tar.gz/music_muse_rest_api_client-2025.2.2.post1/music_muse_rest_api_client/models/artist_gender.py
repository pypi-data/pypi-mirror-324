from enum import Enum


class ArtistGender(str, Enum):
    FEMALE = "female"
    MALE = "male"
    NOT_SPECIFIED = "not_specified"
    OTHER = "other"

    def __str__(self) -> str:
        return str(self.value)
