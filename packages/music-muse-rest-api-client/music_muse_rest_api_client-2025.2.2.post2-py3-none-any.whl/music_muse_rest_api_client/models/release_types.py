from enum import Enum


class ReleaseTypes(str, Enum):
    ALBUM = "album"
    BOOK = "book"
    COMPILATION = "compilation"
    INDEFINITE = "indefinite"
    LIVE = "live"
    MAXI_SINGLE = "maxi_single"
    MINI_ALBUM = "mini_album"
    PODCAST = "podcast"
    REISSUE = "reissue"
    REMIX = "remix"
    SINGLE = "single"

    def __str__(self) -> str:
        return str(self.value)
