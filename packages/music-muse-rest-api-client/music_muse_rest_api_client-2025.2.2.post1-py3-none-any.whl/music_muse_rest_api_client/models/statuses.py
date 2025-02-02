from enum import Enum


class Statuses(str, Enum):
    ACTIVE = "active"
    DELETED = "deleted"
    INACTIVE = "inactive"
    MODERATION = "moderation"

    def __str__(self) -> str:
        return str(self.value)
