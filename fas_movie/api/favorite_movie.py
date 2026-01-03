from fas_movie.database.models import FavoriteMovie
from fas_movie.database.schema import FavoriteMovieInputSchema, FavoriteMovieOutSchema
from fas_movie.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, Depends, APIRouter

favorite_movie_router = APIRouter(prefix='/favorite_movie')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@favorite_movie_router.post('/', response_model=FavoriteMovieOutSchema, summary='Create favorite movie.', tags=['Favorite Movie'])
async def create_favorite_movie(favorite_movie: FavoriteMovieInputSchema, db: Session = Depends(get_db)):
    favorite_movie_db = FavoriteMovie(**favorite_movie.model_dump())
    db.add(favorite_movie_db)
    db.commit()
    db.refresh(favorite_movie_db)
    return favorite_movie_db

@favorite_movie_router.get('/', response_model=List[FavoriteMovieOutSchema], summary='Get all favorite movies.', tags=['Favorite Movie'])
async def favorite_movie_list(db: Session = Depends(get_db)):
    favorite_movies_db = db.query(FavoriteMovie).all()
    if not favorite_movies_db:
        raise HTTPException(status_code=404, detail='No favorite movie yet.')
    return favorite_movies_db

@favorite_movie_router.get('/{favorite_movie_id}/', response_model=FavoriteMovieOutSchema, summary='Get favorite movie by id.', tags=['Favorite Movies'])
async def favorite_movie_detail(favorite_movie_id: int, db: Session = Depends(get_db)):
    favorite_movie_db1 = db.query(FavoriteMovie).filter(FavoriteMovie.id==favorite_movie_id).first()
    if not favorite_movie_db1:
        raise HTTPException(status_code=404, detail='Favorite movie not founded by this id.')
    return favorite_movie_db1

@favorite_movie_router.put('/{favorite_movie_id}/', response_model=dict, summary='Update your favorite movies.', tags=['Favorite Movies'])
async def favorite_movie_update(favorite_movie_id: int, favorite_movie: FavoriteMovieInputSchema, db: Session = Depends(get_db)):
    favorite_movie_db2 = db.query(FavoriteMovie).filter(FavoriteMovie.id==favorite_movie_id).first()
    if not favorite_movie_db2:
        raise HTTPException(status_code=404, detail='Favorite movie not founded with this id.')
    for key, value in favorite_movie.model_dump().items():
        setattr(favorite_movie_db2, key, value)
    db.commit()
    db.refresh(favorite_movie_db2)
    return {'detail': 'Favorite movie has been changed.'}

@favorite_movie_router.delete('/{favorite_movie_id}/', response_model=dict, summary='Delete favorite movies.', tags=['Favorite Movies'])
async def favorite_movie_delete(favorite_movie_id: int, db: Session = Depends(get_db)):
    favorite_movie_db3 = db.query(FavoriteMovie).filter(FavoriteMovie.id==favorite_movie_id).first()
    if not favorite_movie_db3:
        raise HTTPException(status_code=404, detail='Favorite movie not founded by this id.')
    db.delete(favorite_movie_db3)
    db.commit()
    return {'detail': 'Favorite movie has been deleted.'}