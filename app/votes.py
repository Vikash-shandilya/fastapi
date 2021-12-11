from fastapi import FastAPI,APIRouter,HTTPException,Depends
from fastapi.datastructures import DefaultPlaceholder
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from starlette import status
from . import schemas


from . import models,schemas,orm,oauth


router=APIRouter()
@router.post('/votes')
def voting(user:schemas.vote,db:Session=Depends(orm.get_db),userinfo:dict=Depends(oauth.get_current_user)):
    user_id=userinfo.id
    post_check=db.query(models.Post).filter(models.Post.id==user.post_id).first()
    if post_check==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='post not found')

    vote_query=db.query(models.Vote).filter(models.Vote.post_id==user.post_id,models.Vote.user_id==user_id)
    found_vote=vote_query.first()
    
    if(user.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f'so you cant like the post again')
        created_vote=models.Vote(post_id=user.post_id,user_id=user_id)
        db.add(created_vote)
        db.commit()
        return {'detailed':'you have voted successfully'}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='sorry you cant delete a vote ')
        found_vote.delete(synchronize_session=False)
        db.commit()
        return {'details':"you have succesfully deleted your vote"}


