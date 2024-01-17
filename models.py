from typing import Any

from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class SwapiPeople(Base):

    __tablename__ = 'swapi_people'

    id: Mapped[int] = mapped_column(primary_key=True)
    birth_year: Mapped[str] = mapped_column(String(20))
    eye_color: Mapped[str] = mapped_column(String(16))
    films: Mapped[str] = mapped_column(String)
    gender: Mapped[str] = mapped_column(String(20))
    hair_color: Mapped[str] = mapped_column(String(32))
    height: Mapped[str] = mapped_column(String(20))
    homeworld: Mapped[str] = mapped_column(String(32))
    mass: Mapped[str] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(64))
    skin_color: Mapped[str] = mapped_column(String(32))
    species: Mapped[str] = mapped_column(String)
    starships: Mapped[str] = mapped_column(String)
    vehicles: Mapped[str] = mapped_column(String)
