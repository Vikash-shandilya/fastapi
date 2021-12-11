
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from .orm import Base 
from sqlalchemy import Column, Integer,Boolean,String

class Post(Base):# think why it extends to Base class
    __tablename__='posts'
    id=Column(Integer,primary_key=True,nullable=False,index=True)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    postable=Column(Boolean,server_default='True')
    owner_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    owner=relationship('user')

class user(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True,nullable=False)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)

class Vote(Base):
    __tablename__='votes'
    post_id=Column(Integer,primary_key=True,nullable=False)
    user_id=Column(Integer,primary_key=True,nullable=False)
    