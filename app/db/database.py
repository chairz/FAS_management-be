
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config.config import settings

load_dotenv()

SQL_HOST = settings.SQL_HOST
SQL_DATABASE = settings.SQL_DATABASE
SQL_USER = settings.SQL_USER
SQL_PASSWORD = settings.SQL_PASSWORD

if SQL_PASSWORD:
    DATABASE_URL = f'mysql+pymysql://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}/{SQL_DATABASE}'
else:
    DATABASE_URL = f'mysql+pymysql://{SQL_USER}@{SQL_HOST}/{SQL_DATABASE}'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
