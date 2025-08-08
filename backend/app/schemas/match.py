from pydantic import BaseModel


class MatchResult(BaseModel):
    match_id: int
    mode: str
    winner_user_id: int | None


class InventoryItem(BaseModel):
    id: str
    name: str
    rarity: str