from typing import Optional

from pydantic import BaseModel, BaseSettings
from pydantic.fields import Field


class Person(BaseModel):
    """В elastic каждая персона содержит id и full_name."""

    id: str
    name: str


class Genre(BaseModel):
    """В elastic каждый жанр содержит id и full_name."""

    id: str
    name: str


class ElasticMoviesSchemaModel(BaseModel):
    """Модель соответствует схеме индекса movies."""

    id: str
    imdb_rating: float | None = 0.0
    genres: list[Genre] = []
    title: str
    description: Optional[str]
    directors: list[Person] = []
    actors_names: list[str] = []
    writers_names: list[str] = []
    actors: list[Person] = []
    writers: list[Person] = []


class ElasticPersonsSchemaModel(BaseModel):
    """Модель соответствует схеме индекса persons."""

    id: str
    full_name: str


class ElasticGenresSchemaModel(BaseModel):
    """Модель соответствует схеме индекса genres."""

    id: str
    name: str
    description: Optional[str] = ""


class EnvSettings(BaseSettings):
    """Настройки из .env"""

    pg_db_name: str = Field(env="POSTGRES_DB")
    pg_db_user: str = Field(env="POSTGRES_USER")
    pg_db_password: str = Field(env="POSTGRES_PASSWORD")
    pg_db_host: str = Field(env="POSTGRES_DB_HOST")
    pg_db_port: str = Field(env="POSTGRES_DB_PORT")

    es_host: str = Field(env="ES_HOST")
    es_port: int = Field(env="ES_PORT")

    @property
    def es_url(self):
        return f"{self.es_host}:{self.es_port}"

    class Config:
        env_file = ".env"
