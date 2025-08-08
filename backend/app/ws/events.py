import asyncio
from typing import Any, Dict, List

from starlette.websockets import WebSocket

from app.matchmaking.queue import PlayerTicket, queue
from app.ws.manager import room_manager


async def handle_join(ws: WebSocket, payload: Dict[str, Any]) -> None:
    mode = payload.get("mode", "ffa")
    ws_id = getattr(ws.state, "ws_id", None) or room_manager.new_ws_id()
    ws.state.ws_id = ws_id

    await queue.enqueue(mode, PlayerTicket(user_id=None, vk_user_id=None, ws_id=ws_id))
    await room_manager.attach(ws_id, ws)

    # try immediate full room
    formed = await queue.try_form_room(mode)
    if not formed:
        # wait briefly then fill with bots
        await asyncio.sleep(2.0)
        formed = await queue.drain_with_bots(mode)

    if formed:
        room = await room_manager.create_room(mode)
        # place players around arena
        spawn_points = [(2.0, 2.0), (30.0, 2.0), (2.0, 16.0), (30.0, 16.0), (16.0, 9.0), (8.0, 4.0), (24.0, 4.0), (8.0, 14.0), (24.0, 14.0), (16.0, 4.0), (16.0, 14.0), (4.0, 9.0)]
        for i, t in enumerate(formed):
            sx, sy = spawn_points[i % len(spawn_points)]
            room.add_player(player_id=t.ws_id, user_id=t.user_id, x=sx, y=sy)
        await ws.send_json({"type": "event", "event": {"type": "countdown", "payload": {"t": 3}}})


async def handle_input(ws: WebSocket, payload: Dict[str, Any]) -> None:
    ws_id = getattr(ws.state, "ws_id", None)
    if not ws_id:
        return
    # Find the room of this player
    for room in room_manager.rooms.values():
        if ws_id in room.players:
            room.receive_input(ws_id, payload)
            await ws.send_json({"type": "ack", "seq": payload.get("seq")})
            return


async def handle_leave(ws: WebSocket) -> None:
    ws_id = getattr(ws.state, "ws_id", None)
    if not ws_id:
        return
    for room in room_manager.rooms.values():
        if ws_id in room.players:
            room.remove_player(ws_id)
            break
    await room_manager.detach(ws_id)