from fas_movie.database.models import CustomUser
from fas_movie.database.db import SessionLocal
from fastapi import APIRouter, HTTPException, Depends
from fas_movie.database.schema import CustomUserOutSchema, CustomUserInputSchema
from sqlalchemy.orm import Session
from typing import List

users_router = APIRouter(prefix='/users')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@users_router.post('/', response_model=CustomUserOutSchema, summary='Create user', tags=['Users'])
async def create_user(user: CustomUserInputSchema, db: Session = Depends(get_db)):
    user_db = CustomUser(**user.model_dump())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@users_router.get('/', response_model=List[CustomUserOutSchema], summary='Get all users', tags=['Users'])
async def users_list(db: Session = Depends(get_db)):
    users_db = db.query(CustomUser).all()
    if not users_db:
        raise HTTPException(detail='No users.', status_code=404)
    return users_db

@users_router.get('/{user_id}/', response_model=CustomUserOutSchema, summary='Get user by id', tags=['Users'])
async def user_detail(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(CustomUser).filter(CustomUser.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='User not founded with this id.', status_code=404)
    return user_db

@users_router.put('/{user_id/}', response_model=dict, summary='Change user.', tags=['Users'])
async def user_update(user_id: int, user: CustomUserInputSchema, db: Session = Depends(get_db)):
    user_db1 = db.query(CustomUser).filter(CustomUser.id==user_id).first()
    if not user_db1:
        raise HTTPException(status_code=404, detail='User not founded by this id.')
    for key, value in user.model_dump().items():
        setattr(user_db1, key, value)
    db.commit()
    db.refresh(user_db1)
    return {'detail': 'User has been changed.'}

@users_router.delete('/{user_id}/', response_model=dict, summary='Delete user.', tags=['Users'])
async def user_delete(user_id: int, db: Session = Depends(get_db)):
    user_db2 = db.query(CustomUser).filter(CustomUser.id==user_id).first()
    if not user_db2:
        raise HTTPException(status_code=404, detail='User not founded by this id.')
    db.delete(user_db2)
    db.commit()
    return {'detail': 'User has been deleted.'}