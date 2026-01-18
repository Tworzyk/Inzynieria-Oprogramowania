# movie_service/models.py
from sqlalchemy import Column, Integer, String, Text, Date, Table, ForeignKey
from sqlalchemy.orm import relationship

from common.basesql import Base

# Tabela asocjacyjna film-gatunek (w tym samym serwisie)
movie_genres_table = Table(
    "movie_genres",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    release_date = Column(Date, nullable=True)
    age_rating = Column(String(10), nullable=True)  # np. "PG-13", "16+", itp.
    duration_minutes = Column(Integer, nullable=True)

    # np. URL do plakatu
    poster_url = Column(String(512), nullable=True)

    genres = relationship(
        "Genre",
        secondary=movie_genres_table,
        back_populates="movies",
        lazy="joined",
    )

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    movies = relationship(
        "Movie",
        secondary=movie_genres_table,
        back_populates="genres",
    )
