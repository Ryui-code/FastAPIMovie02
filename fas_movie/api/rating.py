from fas_movie.database.models import Rating
from fas_movie.database.schema import RatingOutSchema, RatingInputSchema
from fas_movie.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, Depends, APIRouter

rating_router = APIRouter(prefix='/rating')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@rating_router.post('/', response_model=RatingOutSchema, summary='Create rating.', tags=['Rating'])
async def create_rating(rating: RatingInputSchema, db: Session = Depends(get_db)):
    rating_db = Rating(**rating.model_dump())
    db.add(rating_db)
    db.commit()
    db.refresh(rating_db)
    return rating_db

@rating_router.get('/', response_model=List[RatingOutSchema], summary='Get all ratings.', tags=['Rating'])
async def rating_list(db: Session = Depends(get_db)):
    ratings_db = db.query(Rating).all()
    if not ratings_db:
        raise HTTPException(status_code=404, detail='No ratings yet.')
    return ratings_db

@rating_router.get('/{rating_id}/', response_model=RatingOutSchema, summary='Get rating by id.', tags=['Rating'])
async def rating_detail(rating_id: int, db: Session = Depends(get_db)):
    rating_db1 = db.query(Rating).filter(Rating.id==rating_id).first()
    if not rating_db1:
        raise HTTPException(status_code=404, detail='Rating not founded by this id.')
    return rating_db1

@rating_router.put('/{rating_id}/', response_model=dict, summary='Update your rating.', tags=['Rating'])
async def rating_update(rating_id: int, rating: RatingInputSchema, db: Session = Depends(get_db)):
    rating_db2 = db.query(Rating).filter(Rating.id==rating_id).first()
    if not rating_db2:
        raise HTTPException(status_code=404, detail='Rating not founded with this id.')
    for key, value in rating.model_dump().items():
        setattr(rating_db2, key, value)
    db.commit()
    db.refresh(rating_db2)
    return {'detail': 'Rating has been changed.'}

@rating_router.delete('/{rating_id}/', response_model=dict, summary='Delete rating.', tags=['Rating'])
async def rating_delete(rating_id: int, db: Session = Depends(get_db)):
    rating_db3 = db.query(Rating).filter(Rating.id==rating_id).first()
    if not rating_db3:
        raise HTTPException(status_code=404, detail='Rating not founded by this id.')
    db.delete(rating_db3)
    db.commit()
    return {'detail': 'Rating has been deleted.'}