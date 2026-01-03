from pydantic import Field, EmailStr
from typing import Optional
from pydantic import BaseModel
from enum import Enum
from datetime import date

class StatusChoices(str, Enum):
    GUEST = 'Guest'
    AUTHOR = 'Author'

class TypesChoices(str, Enum):
    p144 = '144p'
    p270 = '270p'
    p360 = '360p'
    p480 = '480p'
    p720 = '720p'
    p1080 = '1080p'

class GenreChoices(str, Enum):
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

class CustomUserLoginSchema(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(ge=6)

class CustomUserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    age: Optional[int]
    phone_number: Optional[str]
    status: StatusChoices = StatusChoices.GUEST
    data_registered: date
class CustomUserInputSchema(BaseModel):
    username: str | int = Field(min_length=3, max_length=30)
    password: str = Field(min_length=6)
    email: EmailStr
    age: Optional[int] = Field(ge=18, le=100)
    phone_number: Optional[str]
    status: StatusChoices = StatusChoices.GUEST

class MovieOutSchema(BaseModel):
    id: int
    name: str
    genre: GenreChoices
    description: str
    actors_id: int
    trailer_id: int
    types: TypesChoices
    duration: int
    country: str
    rating_id: int
    created_date: date
class MovieInputSchema(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    genre: GenreChoices
    description: str
    actors_id: int
    trailer_id: int
    types: TypesChoices
    duration: int
    country: str
    rating_id: int

class ActorOutSchema(BaseModel):
    id: int
    actor_id: int
    full_name: str
    age: int
    phone_number: Optional[int]
    bio: str
    photo_id: int
    created_date: date
class ActorInputSchema(BaseModel):
    actor_id: int
    full_name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=18, le=60)
    phone_number: Optional[int]
    bio: str
    photo_id: int

class RatingOutSchema(BaseModel):
    id: int
    movie_id: int
    stars: int
    description: str
    created_date: date
class RatingInputSchema(BaseModel):
    movie_id: int
    stars: int = Field(ge=0, le=5)
    description: str

class FavoriteMovieOutSchema(BaseModel):
    id: int
    movie_id: int
class FavoriteMovieInputSchema(BaseModel):
    movie_id: int