from fastapi import FastAPI,staticfiles,HTTPException,Depends,APIRouter
from sqlalchemy.orm.session import Session
from starlette import status
from .. import orm ,schemas,models,utils,oauth
from sqlalchemy.orm import Session


router=APIRouter(tags=['authentication'])

@router.post('/login',response_model=schemas.Token)
def login(usercredential:schemas.usercred,db:Session=Depends(orm.get_db)):# learn about OAuth2PasswordRequestForm
    user=db.query(models.user).filter(models.user.email==usercredential.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'invalid credential')
    
    if not utils.verify_password(usercredential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invalid credential")
    token=oauth.token_generate(data={'user_id':user.id})
    return {'generated_token':token ,"token_type":"bearer"}