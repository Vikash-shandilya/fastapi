from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from . config import settings

SQLALCHEMY_DATABASE_URL=f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# SQLALCHEMY_DATABASE_URL="postgresql://<username>:<password>@<ipaddress>/<databasename>"
# this is unique url that is used to connect to database
print(SQLALCHEMY_DATABASE_URL)
engine=create_engine(SQLALCHEMY_DATABASE_URL)# responsible for connecting sqlalchemy to postgresql
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)# each instance of sessionlocal will be a session 
Base=declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
