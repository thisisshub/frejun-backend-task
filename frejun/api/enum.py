from enum import Enum


class BookingStatus(Enum):
    RAC = "RAC"
    WAITING_LIST = "WAITING_LIST"
    CONFIRMED = "CONFIRMED"

class BerthType(Enum):
    LOWER = "LOWER"
    MIDDLE = "MIDDLE"
    UPPER = "UPPER"
    SIDE_LOWER = "SIDE_LOWER"
    NO_BERTH = "NO_BERTH"
