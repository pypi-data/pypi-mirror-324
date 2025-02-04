from enum import Enum


class SubscriptionType(str, Enum):
    ADVANCED = "advanced"
    BASIC = "basic"
    BUSINESS = "business"
    EDU5 = "edu5"
    ENTERPRISE = "enterprise"
    ESSENTIAL = "essential"
    PROFESSIONAL = "professional"

    def __str__(self) -> str:
        return str(self.value)
