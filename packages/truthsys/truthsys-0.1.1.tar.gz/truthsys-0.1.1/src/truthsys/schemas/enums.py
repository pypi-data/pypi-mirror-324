from enum import Enum

class PredictionEnum(str, Enum):
    supports = "SUPPORTS"
    not_enough_info = "NOT ENOUGH INFO"
    refutes = "REFUTES"

class PredictionNumEnum(int, Enum):
    refutes = 0
    not_enough_info = 1
    supports = 2