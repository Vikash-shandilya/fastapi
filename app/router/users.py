from fastapi import FastAPI , status ,Response,HTTPException,Depends,APIRouter
from app import models,schemas,utils
#from .. import models,schemas,utils
from sqlalchemy.orm import Session
#from ...orm import get_db
from app.orm import get_db
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND 

router=APIRouter(
    prefix='/users',
    tags=["Users"]
)


@router.post("/",status_code=HTTP_201_CREATED,response_model=schemas.userout)
def root(newuser:schemas.usersin,db: Session = Depends(get_db)):
    #hash the password

    newuser.password=utils.makehash(newuser.password)
    create_users=models.user(**newuser.dict())
    db.add(create_users)
    db.commit()
    db.refresh(create_users)
    return create_users

@router.get('/{id}',response_model=schemas.userout)
def get_user_info(id:int,db: Session = Depends(get_db)):
    user_info=db.query(models.user).filter(models.user.id==id).first()
    if not user_info:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,detail=f"sorry user not found")
    return user_info