from uuid import UUID

from common import Base


class FilmProgressView(Base):
    user_id: int
    film_id: UUID
    film_position_ms: int
