from dataclasses import dataclass
from random import random
from typing import Dict, List, Tuple


@dataclass
class BotState:
    bot_id: str
    cooldown: float = 0.0


class BotController:
    def __init__(self, skill: float = 0.6) -> None:
        self.skill = skill
        self.bots: Dict[str, BotState] = {}

    def ensure(self, bot_id: str) -> None:
        if bot_id not in self.bots:
            self.bots[bot_id] = BotState(bot_id)

    def decide(self, bot_id: str, dt: float, self_pos: Tuple[float, float], targets: List[Tuple[float, float]]):
        self.ensure(bot_id)
        st = self.bots[bot_id]
        st.cooldown = max(0.0, st.cooldown - dt)

        move_x, move_y = 0.0, 0.0
        fire = False
        if targets:
            # naive seek nearest
            tx, ty = min(targets, key=lambda p: (p[0]-self_pos[0])**2 + (p[1]-self_pos[1])**2)
            move_x = 1.0 if tx > self_pos[0] else -1.0
            move_y = 1.0 if ty > self_pos[1] else -1.0
            if st.cooldown <= 0.0 and random() < self.skill:
                fire = True
                st.cooldown = 0.5 + (1.0 - self.skill)  # worse skill => longer cooldown
        return {"move": {"x": move_x, "y": move_y}, "fire": fire}


bot_controller = BotController()