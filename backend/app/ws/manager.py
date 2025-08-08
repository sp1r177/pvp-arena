import asyncio
from typing import Any, Callable, Dict
from uuid import uuid4

from starlette.websockets import WebSocket

from app.core.config import settings
from app.game.engine import GameRoom


class RoomManager:
    def __init__(self) -> None:
        self.rooms: Dict[str, GameRoom] = {}
        self.connections: Dict[str, WebSocket] = {}
        self.room_tasks: Dict[str, asyncio.Task] = {}
        self.lock = asyncio.Lock()

    def new_ws_id(self) -> str:
        return str(uuid4())

    async def create_room(self, mode: str) -> GameRoom:
        room_id = str(uuid4())
        room = GameRoom(room_id=room_id, mode=mode)
        self.rooms[room_id] = room

        async def send_snapshot(snapshot: dict):
            # broadcast to room participants
            payload = {"type": "state", **snapshot}
            await self.broadcast(room_id, payload)

        task = asyncio.create_task(room.run(send_snapshot))
        self.room_tasks[room_id] = task
        return room

    async def broadcast(self, room_id: str, message: dict) -> None:
        # naive broadcast to all connections belonging to players in the room
        room = self.rooms.get(room_id)
        if not room:
            return
        for pid in list(room.players.keys()):
            ws = self.connections.get(pid)
            if ws is not None:
                try:
                    await ws.send_json(message)
                except Exception:
                    pass

    async def attach(self, player_id: str, websocket: WebSocket) -> None:
        self.connections[player_id] = websocket

    async def detach(self, player_id: str) -> None:
        self.connections.pop(player_id, None)


room_manager = RoomManager()