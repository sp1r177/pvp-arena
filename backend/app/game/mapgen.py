import random
from typing import List, Tuple

Cell = int  # 0 empty, 1 wall


def generate_map(width: int = 32, height: int = 18, wall_prob: float = 0.12) -> List[List[Cell]]:
    grid = [[0 for _ in range(width)] for _ in range(height)]

    # Add random walls with border kept empty
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if random.random() < wall_prob:
                grid[y][x] = 1

    # Carve safe spawn corners and block straight lines between them
    spawns = [(2, 2), (width - 3, height - 3), (2, height - 3), (width - 3, 2)]
    for sx, sy in spawns:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if 0 <= sx + dx < width and 0 <= sy + dy < height:
                    grid[sy + dy][sx + dx] = 0

    # Block straight corridors between left-right and top-bottom centers
    cx, cy = width // 2, height // 2
    for x in range(width):
        grid[cy][x] = max(grid[cy][x], 1) if x not in (cx - 1, cx, cx + 1) else 0
    for y in range(height):
        grid[y][cx] = max(grid[y][cx], 1) if y not in (cy - 1, cy, cy + 1) else 0

    return grid


def hash_map(grid: List[List[Cell]]) -> str:
    # Simple hash for client-side caching
    flat = ''.join(''.join(str(c) for c in row) for row in grid)
    return hex(abs(hash(flat)))[2:]