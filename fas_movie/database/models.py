from fas_movie.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, Integer, String, Date, Text, ForeignKey
from typing import List, Optional
from enum import Enum as PyEnum
from datetime import date

class StatusChoices(str, PyEnum):
    GUEST = 'Guest'
    AUTHOR = 'Author'

class TypesChoices(str, PyEnum):
    p144 = '144p'
    p270 = '270p'
    p360 = '360p'
    p480 = '480p'
    p720 = '720p'
    p1080 = '1080p'

class GenreChoices(str, PyEnum):
    ACTION = "Action"
    ADVENTURE = "Adventure"
    COMEDY = "Comedy"
    DRAMA = "Drama"
    HORROR = "Horror"
    THRILLER = "Thriller"
    ROMANCE = "Romance"
    SCI_FI = "Sci-Fi"
    FANTASY = "Fantasy"
    DOCUMENTARY = "Documentary"
    ANIMATION = "Animation"
    CRIME = "Crime"
    MYSTERY = "Mystery"
    FAMILY = "Family"
    WAR = "War"

class CustomUser(Base):
    __tablename__ = 'custom_user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.GUEST)
    data_registered: Mapped[date] = mapped_column(Date, default=date.today)

    users_actor: Mapped['Actor'] = relationship('Actor', back_populates='user', uselist=False)
    users_token: Mapped[List['CustomUserRefreshToken']] = relationship(
        'CustomUserRefreshToken',
        back_populates='token_user',
        cascade='all, delete-orphan'
    )

    def __str__(self):
        return f'{self.username}, {self.email}'

class CustomUserRefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('custom_user.id'))
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[date] = mapped_column(Date, default=date.today())

    token_user: Mapped[CustomUser] = relationship(CustomUser, back_populates='users_token')

class Movie(Base):
    __tablename__ = 'movie'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    genre: Mapped[GenreChoices] = mapped_column(Enum(GenreChoices))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    types: Mapped[TypesChoices] = mapped_column(Enum(TypesChoices), default=TypesChoices.p720)
    duration: Mapped[Optional[int]] = mapped_column(Integer)
    country: Mapped[str] = mapped_column(String, nullable=True)
    created_date: Mapped[date] = mapped_column(Date, default=date.today())

    trailer: Mapped['MovieTrailer'] = relationship('MovieTrailer', back_populates='movies_trailer', uselist=False)
    actors: Mapped[List['Actor']] = relationship('Actor', back_populates='movies_actors')
    favorite_movie: Mapped[List['FavoriteMovie']] = relationship('FavoriteMovie', back_populates='favorite_movie')
    rating: Mapped[List['Rating']] = relationship('Rating', back_populates='movies_rating')

class MovieTrailer(Base):
    __tablename__ = 'movie_trailer'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey('movie.id'))
    trailer: Mapped[str] = mapped_column(String)

    movies_trailer: Mapped[Movie] = relationship(Movie, back_populates='trailer')

class Actor(Base):
    __tablename__ = 'actor'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('custom_user.id'))
    movie_id: Mapped[int] = mapped_column(ForeignKey('movie.id'))
    full_name: Mapped[str] = mapped_column(String, nullable=True)
    age: Mapped[int] = mapped_column(Integer)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    created_date: Mapped[date] = mapped_column(Date, default=date.today())

    photo: Mapped[ActorPhoto] = relationship('ActorPhoto', back_populates='actor', uselist=False)
    user: Mapped[CustomUser] = relationship(CustomUser, back_populates='users_actor')
    movies_actors: Mapped[Movie] = relationship(Movie, back_populates='actors')

    def __repr__(self):
        return f'{self.full_name}'

class ActorPhoto(Base):
    __tablename__ = 'actor_photo'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    actor_id: Mapped[int] = mapped_column(ForeignKey('actor.id'))
    photo: Mapped[str] = mapped_column(String)

    actor: Mapped[Actor] = relationship(Actor, back_populates='photo')

class Rating(Base):
    __tablename__ = 'rating'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey('movie.id'))
    stars: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_date: Mapped[date] = mapped_column(Date, default=date.today())

    movies_rating: Mapped[Movie] = relationship(Movie, back_populates='rating')

class FavoriteMovie(Base):
    __tablename__ = 'favorite_movie'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey('movie.id'))

    favorite_movie: Mapped[Movie] = relationship(Movie, back_populates='favorite_movie')