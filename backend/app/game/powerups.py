import random
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Powerup:
    kind: str
    x: float
    y: float


KINDS = ["heal", "speed", "damage"]


def spawn_powerups(num: int, width: int, height: int) -> List[Powerup]:
    out: List[Powerup] = []
    for _ in range(num):
        out.append(Powerup(kind=random.choice(KINDS), x=random.uniform(1, width - 1), y=random.uniform(1, height - 1)))
    return out