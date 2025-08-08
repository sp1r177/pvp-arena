from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models so Alembic can autogenerate
from app.models import user, match, player_state  # noqa: F401