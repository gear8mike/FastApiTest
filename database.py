from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#example of sql_url
#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-addresss/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:112121@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()