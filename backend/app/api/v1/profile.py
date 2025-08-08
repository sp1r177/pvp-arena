from fastapi import APIRouter
from app.schemas.match import InventoryItem

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/inventory", response_model=list[InventoryItem])
async def get_inventory():
    return [
        {"id": "skin_basic", "name": "Basic Suit", "rarity": "common"},
        {"id": "trail_red", "name": "Red Trail", "rarity": "rare"},
    ]