from datetime import timedelta, datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from fas_movie.database.db import SessionLocal
from fas_movie.database.models import CustomUser, CustomUserRefreshToken
from fas_movie.database.schema import CustomUserInputSchema, CustomUserLoginSchema
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fas_movie.config import ALGORITHM, ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME, SECRET_KEY
from jose import jwt

auth_router = APIRouter(prefix='/auth', tags=['Auth'])

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_LIFETIME)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))
@auth_router.post('/register/', response_model=dict, tags=['Auth'])
async def register(user: CustomUserInputSchema, db: Session = Depends(get_db)):
    username_db = db.query(CustomUser).filter(CustomUser.username==user.username).first()
    email_db = db.query(CustomUser).filter(CustomUser.email==user.email).first()
    if username_db:
        raise HTTPException(status_code=400, detail='This username is already exists.')
    if email_db:
        raise HTTPException(status_code=400, detail='This email already exists.')
    hashed_password = get_password_hash(user.password)
    user_db = CustomUser(
        username=user.username,
        email=user.email,
        password=hashed_password,
        age=user.age,
        phone_number=user.phone_number,
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return {'detail': 'Successfully registered.'}

@auth_router.post('/login/', response_model=dict, tags=['Auth'])
async def login(user: CustomUserLoginSchema, db: Session = Depends(get_db)):
    username_db1 = db.query(CustomUser).filter(CustomUser.username==user.username).first()
    if not username_db1 or not verify_password(user.password, username_db1.password):
        raise HTTPException(status_code=401, detail='Invalid credentials.')
    access_token = create_access_token({'sub': username_db1.username})
    refresh_token = create_refresh_token({'sub': username_db1.username})
    token_db = CustomUserRefreshToken(
        user_id=username_db1.id,
        token=refresh_token
    )
    db.add(token_db)
    db.commit()
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer'
    }

@auth_router.post('/logout/', tags=['Auth'])
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    old_token = db.query(CustomUserRefreshToken).filter(CustomUserRefreshToken.token==refresh_token).first()
    if not old_token:
        raise HTTPException(status_code=401, detail='Invalid token.')
    db.delete(old_token)
    db.commit()
    return {'detail': 'Successfully logged out.'}

@auth_router.post('/refresh')
async def refresh(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(CustomUserRefreshToken).filter(CustomUserRefreshToken.token==refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=402, detail='Token already exists.')
    access_token = create_access_token({"sub": stored_token})
    return {'access_token': access_token, 'token_type': 'Bearer'}