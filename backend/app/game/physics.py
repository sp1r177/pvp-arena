from typing import Tuple


def circles_intersect(a_pos: Tuple[float, float], a_r: float, b_pos: Tuple[float, float], b_r: float) -> bool:
    dx = a_pos[0] - b_pos[0]
    dy = a_pos[1] - b_pos[1]
    return dx * dx + dy * dy <= (a_r + b_r) * (a_r + b_r)