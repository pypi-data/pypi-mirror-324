from enum import Enum


class ContactType(str, Enum):
    AUTO = "auto"
    CUSTOM = "custom"

    def __str__(self) -> str:
        return str(self.value)
