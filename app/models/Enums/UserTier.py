from enum import Enum


class UserTier(str, Enum):
    BASIC = "basic"
    PREMIUM = "premium"
