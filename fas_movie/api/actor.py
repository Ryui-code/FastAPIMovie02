from fas_movie.database.models import Actor
from fas_movie.database.schema import ActorOutSchema, ActorInputSchema
from fas_movie.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, Depends, APIRouter

actor_router = APIRouter(prefix='/actor')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@actor_router.post('/', response_model=ActorOutSchema, summary='Create actor.', tags=['Actor'])
async def create_actor(actor: ActorInputSchema, db: Session = Depends(get_db)):
    actor_db = Actor(**actor.model_dump())
    db.add(actor_db)
    db.commit()
    db.refresh(actor_db)
    return actor_db

@actor_router.get('/', response_model=List[ActorOutSchema], summary='Get all actors.', tags=['Actor'])
async def actor_list(db: Session = Depends(get_db)):
    actors_db = db.query(Actor).all()
    if not actors_db:
        raise HTTPException(status_code=404, detail='No actors yet.')
    return actors_db

@actor_router.get('/{actor_id}/', response_model=ActorOutSchema, summary='Get actor by id.', tags=['Actor'])
async def actor_detail(actor_id: int, db: Session = Depends(get_db)):
    actor_db1 = db.query(Actor).filter(Actor.id==actor_id).first()
    if not actor_db1:
        raise HTTPException(status_code=404, detail='Actor not founded by this id.')
    return actor_db1

@actor_router.put('/{actor_id}/', response_model=dict, summary='Update your actor.', tags=['Actor'])
async def actor_update(actor_id: int, actor: ActorInputSchema, db: Session = Depends(get_db)):
    actor_db2 = db.query(Actor).filter(Actor.id==actor_id).first()
    if not actor_db2:
        raise HTTPException(status_code=404, detail='Actor not founded with this id.')
    for key, value in actor.model_dump().items():
        setattr(actor_db2, key, value)
    db.commit()
    db.refresh(actor_db2)
    return {'detail': 'Actor has been changed.'}

@actor_router.delete('/{actor_id}/', response_model=dict, summary='Delete actor.', tags=['Actor'])
async def actor_delete(actor_id: int, db: Session = Depends(get_db)):
    actor_db3 = db.query(Actor).filter(Actor.id==actor_id).first()
    if not actor_db3:
        raise HTTPException(status_code=404, detail='Actor not founded by this id.')
    db.delete(actor_db3)
    db.commit()
    return {'detail': 'Actor has been deleted.'}