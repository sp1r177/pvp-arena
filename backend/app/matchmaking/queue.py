import asyncio
from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Optional

from app.core.config import settings


@dataclass
class PlayerTicket:
    user_id: Optional[int]
    vk_user_id: str | None
    ws_id: str  # internal connection id


class MatchmakingQueue:
    def __init__(self) -> None:
        self.queues: Dict[str, Deque[PlayerTicket]] = {
            "ffa": deque(),
            "duo": deque(),
        }
        self.lock = asyncio.Lock()

    def capacity_for_mode(self, mode: str) -> int:
        return settings.ROOM_CAPACITY_FFA if mode == "ffa" else settings.ROOM_CAPACITY_DUO

    async def enqueue(self, mode: str, ticket: PlayerTicket) -> None:
        async with self.lock:
            self.queues[mode].append(ticket)

    async def try_form_room(self, mode: str) -> List[PlayerTicket] | None:
        async with self.lock:
            q = self.queues[mode]
            cap = self.capacity_for_mode(mode)
            if len(q) >= cap:
                players = [q.popleft() for _ in range(cap)]
                return players
            return None

    async def drain_with_bots(self, mode: str) -> List[PlayerTicket] | None:
        async with self.lock:
            q = self.queues[mode]
            cap = self.capacity_for_mode(mode)
            if not q:
                return None
            players: List[PlayerTicket] = list(q)
            q.clear()
            # Fill with bots if enabled
            if settings.BOT_FILL and len(players) < cap:
                missing = cap - len(players)
                for i in range(missing):
                    players.append(PlayerTicket(user_id=None, vk_user_id=None, ws_id=f"bot-{mode}-{i}"))
            return players


queue = MatchmakingQueue()