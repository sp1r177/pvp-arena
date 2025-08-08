import asyncio
import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from app.core.config import settings
from app.game.physics import circles_intersect
from app.game.mapgen import generate_map, hash_map
from app.matchmaking.bots import bot_controller


@dataclass
class Player:
    id: str
    user_id: int | None
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    hp: int = 100
    kills: int = 0
    alive: bool = True


@dataclass
class Bullet:
    id: int
    x: float
    y: float
    vx: float
    vy: float
    owner_id: str
    ttl: float = 1.0


@dataclass
class GameRoom:
    room_id: str
    mode: str
    players: Dict[str, Player] = field(default_factory=dict)
    bullets: List[Bullet] = field(default_factory=list)
    inputs: Dict[str, dict] = field(default_factory=dict)
    started_at: float = field(default_factory=lambda: time.time())
    finished: bool = False

    # map
    grid: List[List[int]] = field(default_factory=lambda: generate_map())
    map_hash: str = field(init=False)

    def __post_init__(self) -> None:
        self.map_hash = hash_map(self.grid)

    async def run(self, send_snapshot_cb):
        tick_rate = settings.TICK_RATE
        tick_dt = 1.0 / tick_rate
        max_duration = settings.MATCH_DURATION_SEC
        bullet_id_seq = 0

        while not self.finished:
            start = time.time()
            # Check duration
            if start - self.started_at >= max_duration:
                self.finished = True

            # Bot AI: synthesize inputs for bot players
            for pid, p in self.players.items():
                if pid.startswith("bot-") and p.alive:
                    targets = [(op.x, op.y) for k, op in self.players.items() if k != pid and op.alive]
                    decision = bot_controller.decide(pid, tick_dt, (p.x, p.y), targets)
                    self.inputs[pid] = {"move": decision["move"], "fire": decision["fire"]}

            # Apply inputs
            for pid, inp in list(self.inputs.items()):
                p = self.players.get(pid)
                if not p or not p.alive:
                    continue
                mv = inp.get("move", {"x": 0.0, "y": 0.0})
                p.vx = float(mv.get("x", 0.0)) * 6.0
                p.vy = float(mv.get("y", 0.0)) * 6.0
                if inp.get("fire"):
                    # spawn bullet
                    speed = 16.0
                    bx, by = p.x, p.y
                    # shoot forward along velocity or upward if idle
                    dir_x, dir_y = (p.vx, p.vy)
                    if abs(dir_x) + abs(dir_y) < 0.01:
                        dir_x, dir_y = 0.0, -1.0
                    mag = max((dir_x ** 2 + dir_y ** 2) ** 0.5, 1.0)
                    bullet = Bullet(
                        id=bullet_id_seq,
                        x=bx,
                        y=by,
                        vx=speed * dir_x / mag,
                        vy=speed * dir_y / mag,
                        owner_id=pid,
                        ttl=1.5,
                    )
                    self.bullets.append(bullet)
                    bullet_id_seq += 1

            # Integrate players
            for p in self.players.values():
                if not p.alive:
                    continue
                p.x += p.vx * tick_dt
                p.y += p.vy * tick_dt
                # Clamp arena bounds
                p.x = max(1.0, min(31.0, p.x))
                p.y = max(1.0, min(17.0, p.y))

            # Integrate bullets
            next_bullets: List[Bullet] = []
            for b in self.bullets:
                b.ttl -= tick_dt
                if b.ttl <= 0:
                    continue
                b.x += b.vx * tick_dt
                b.y += b.vy * tick_dt
                # Check hits
                hit = False
                for p in self.players.values():
                    if not p.alive or p.id == b.owner_id:
                        continue
                    if circles_intersect((p.x, p.y), 0.5, (b.x, b.y), 0.2):
                        p.hp -= 25
                        if p.hp <= 0:
                            p.alive = False
                            self.players[b.owner_id].kills += 1
                        hit = True
                        break
                if not hit:
                    next_bullets.append(b)
            self.bullets = next_bullets

            # Broadcast snapshot each tick (could be throttled to 200-300ms)
            await send_snapshot_cb(self.snapshot())

            # sleep until next tick
            elapsed = time.time() - start
            await asyncio.sleep(max(0.0, tick_dt - elapsed))

    def snapshot(self) -> dict:
        return {
            "t": int((time.time() - self.started_at) * settings.TICK_RATE),
            "players": [
                {"id": p.id, "x": p.x, "y": p.y, "hp": p.hp, "kills": p.kills, "alive": p.alive}
                for p in self.players.values()
            ],
            "bullets": [
                {"id": b.id, "x": b.x, "y": b.y}
                for b in self.bullets
            ],
            "mapHash": self.map_hash,
            "timeLeft": max(0, settings.MATCH_DURATION_SEC - int(time.time() - self.started_at)),
        }

    def add_player(self, player_id: str, user_id: int | None, x: float, y: float) -> None:
        self.players[player_id] = Player(id=player_id, user_id=user_id, x=x, y=y)

    def remove_player(self, player_id: str) -> None:
        if player_id in self.players:
            del self.players[player_id]

    def receive_input(self, player_id: str, payload: dict) -> None:
        self.inputs[player_id] = payload