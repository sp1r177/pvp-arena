from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PlayerStateSnapshot(Base):
    __tablename__ = "player_state_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id", ondelete="CASCADE"))
    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    t: Mapped[int] = mapped_column(Integer)  # tick index
    payload_json: Mapped[str] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)