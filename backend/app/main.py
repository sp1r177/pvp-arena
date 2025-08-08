from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.auth import router as auth_router
from app.api.v1.profile import router as profile_router
from app.ws.events import handle_join, handle_input, handle_leave

app = FastAPI(title="VK PvP Arena API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(profile_router, prefix="/api/v1")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            kind = data.get("type") or data.get("event") or data.get("action") or ""
            payload = data.get("payload") or data
            if data.get("join") or kind == "join" or payload.get("mode"):
                await handle_join(websocket, payload)
            elif data.get("input") or kind == "input" or payload.get("move") is not None:
                await handle_input(websocket, payload)
            elif data.get("leave") or kind == "leave":
                await handle_leave(websocket)
    except WebSocketDisconnect:
        await handle_leave(websocket)