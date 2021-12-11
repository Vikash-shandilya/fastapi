from pydantic import BaseModel,EmailStr
from sqlalchemy.engine import base
from sqlalchemy.sql.expression import true
# from app import votes

#from app.models import Vote


# class for returning owner(relationship) and think why this class is not working

class ownerinfo(BaseModel):
    name:str
    email:EmailStr
    class config:
        orm_mode=True


class postbase(BaseModel):# this class is actually used for validation in our post 
    title:str# this is inherited from pydantic basemodel and used for validation
    content:str
    postable:bool=True
    
    #rating:Optional[int]=None# so this is actually used to make option that means
    #if i want to post or not post in both case it should be ok but you have to import it 


class postcreate(postbase):
    pass

class postupdate(postbase):
    pass

# class postupdate(BaseModel):
#     postbase:bool=True# if we do this then user cant update his post he just can choose whether he should post it or not

class userout(BaseModel):
    name:str
    email:str
    id:int

    class Config:
        orm_mode=True


class post(BaseModel):
    title:str
    content:str
    postable:bool
    owner:userout
    class Config:
        orm_mode=True



class usersin(BaseModel):
    name:str
    email:str
    password:str

class vote(BaseModel):
    post_id:int
    dir:int


        


# for authentication
class usercred(BaseModel):
    email:EmailStr
    password:str

#for token

class Token(BaseModel):
    generated_token:str
    token_type:str
    class Config:
        orm_mode=True


class postfinal(BaseModel):
    Post:post
    votes:int
    class Config:
        orm_mode=True
        























