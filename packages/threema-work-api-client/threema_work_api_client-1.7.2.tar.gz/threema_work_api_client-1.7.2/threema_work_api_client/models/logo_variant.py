from enum import Enum


class LogoVariant(str, Enum):
    DARK = "dark"
    LIGHT = "light"

    def __str__(self) -> str:
        return str(self.value)
