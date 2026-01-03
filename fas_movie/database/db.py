from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base

db_url = 'postgresql://postgres:1wprjenuxhskaRRlet@localhost/fas_movie'

engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()