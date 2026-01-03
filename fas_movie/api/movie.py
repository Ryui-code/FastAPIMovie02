from fas_movie.database.models import Movie, GenreChoices
from fas_movie.database.schema import MovieOutSchema, MovieInputSchema
from fas_movie.database.db import SessionLocal
from sqlalchemy.orm import Session, Query
from typing import List
from fastapi import HTTPException, Depends, APIRouter

movie_router = APIRouter(prefix='/movie')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@movie_router.post('/', response_model=MovieOutSchema, summary='Create movie.', tags=['Movie'])
async def create_movie(movie: MovieInputSchema, db: Session = Depends(get_db)):
    movie_db2 = Movie(**movie.model_dump())
    db.add(movie_db2)
    db.commit()
    db.refresh(movie_db2)
    return movie_db2

@movie_router.get('/', response_model=List[MovieOutSchema], summary='Get all movies.', tags=['Movie'])
async def movies_list(db: Session = Depends(get_db)):
    movies_db = db.query(Movie).all()
    if not movies_db:
        raise HTTPException(status_code=404, detail='No movies yet.')
    return movies_db

@movie_router.get('/{movie_id}/', response_model=MovieOutSchema, summary='Get movie by id.', tags=['Movie'])
async def movie_detail(movie_id: int, db: Session = Depends(get_db)):
    movie_db = db.query(Movie).filter(Movie.id==movie_id).first()
    if not movie_db:
        raise HTTPException(status_code=404, detail='Movie not founded by this id.')
    return movie_db

@movie_router.get("/by-genre/", response_model=List[MovieOutSchema], summary='Get movies by genre.', tags=['Movie'])
async def movies_list_by_genre(genre: GenreChoices, db: Session = Depends(get_db)):
    movies_db1 = db.query(Movie).filter(Movie.genre==genre).all()
    if not movies_db1:
        raise HTTPException(status_code=404, detail='Movie not founded with this genre.')
    return movies_db1

@movie_router.put('/{movie_id}/', response_model=dict, summary='Update your movie.', tags=['Movie'])
async def movie_update(movie_id: int, movie: MovieInputSchema, db: Session = Depends(get_db)):
    movie_db3 = db.query(Movie).filter(Movie.id==movie_id).first()
    if not movie_db3:
        raise HTTPException(status_code=404, detail='Movie not founded with this id.')
    for key, value in movie.model_dump().items():
        setattr(movie_db3, key, value)
    db.commit()
    db.refresh(movie_db3)
    return {'detail': 'Movie has been changed.'}

@movie_router.delete('/{movie_id}/', response_model=dict, summary='Delete movie.', tags=['Movie'])
async def movie_delete(movie_id: int, db: Session = Depends(get_db)):
    movie_db4 = db.query(Movie).filter(Movie.id==movie_id).first()
    if not movie_db4:
        raise HTTPException(status_code=404, detail='Movie not founded by this id.')
    db.delete(movie_db4)
    db.commit()
    return {'detail': 'Movie has been deleted.'}