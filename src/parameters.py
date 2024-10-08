
from dataclasses import dataclass


@dataclass
class Parameters:
    BANK_COST: int = 4
    HOUSES_ON_START: int = 2
    CITIES_ON_START: int = 0
    WIN_SCORE: int = 4
    MAX_OF_RESOURCE: int = 5


PARAMETERS = Parameters()
