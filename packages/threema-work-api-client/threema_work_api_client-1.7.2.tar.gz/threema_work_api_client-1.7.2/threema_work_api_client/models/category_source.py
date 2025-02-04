from enum import Enum


class CategorySource(str, Enum):
    CUSTOM = "custom"
    MDM = "mdm"

    def __str__(self) -> str:
        return str(self.value)
