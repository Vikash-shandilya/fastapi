from fastapi import FastAPI , status ,Response,HTTPException,Depends,APIRouter
from sqlalchemy.sql.expression import outerjoin
from .. import models,schemas,utils,oauth
from sqlalchemy.orm import Session
from ..orm import get_db
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND 
from typing import List, Optional
from sqlalchemy import func

router=APIRouter(
    prefix='/posts',
    tags=["Posts"]
)


@router.get('/',response_model=List[schemas.postfinal])

def get_posts(db: Session = Depends(get_db),username:int=Depends(oauth.get_current_user),
limit:int=10,skip:int=0,search:Optional[str]=''):
    # curser.execute(" SELECT * FROM info")
    # post=curser.fetchall()

    # get2this=db.query(models.Post).all()  
    Posts=db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote,models.Post.id==models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    

    return  Posts

@router.post("/createpost",status_code=status.HTTP_201_CREATED,response_model=schemas.post)# we changed the status code 200 to 201 because whenever post is created 201 statuscode should be sent a/q documentation
def create(new_post:schemas.postcreate,db: Session = Depends(get_db),username:dict=Depends(oauth.get_current_user)):# here we cretaed a variable new_post and assign it to our class post we put parameter new_post:post this will validate whtaever we inpu using front end or postman(through body and raw)
    # print(new_post)#so now everything will be done by this class only actually there is one method
    # #new_post.dict() this will convert our pydantic model into dictionary
    
    # curser.execute("INSERT INTO info(title,content,postable) VALUES(%s,%s,%s)RETURNING *",(new_post.title,new_post.content,new_post.postable))# so this is used for inserting input into database by frontend
    # cretaed_post=curser.fetchone()# this is used to return one post that is created obviously one more thing to fetch the post we have to first return that
    # conn.commit()# to save changes into database we have to acually commit 
    
    created_post=models.Post(owner_id=username.id,**new_post.dict())# title=new_post.title,content=new_post.content,postable=new_post.postable instead of this we can use dict unpacking
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post


@router.get("/{id}",response_model=schemas.post)# this is for getting specific posts 
def get_post(id,db: Session = Depends(get_db),username:str=Depends(oauth.get_current_user)):#,response:Response
    
    # curser.execute("SELECT * FROM info WHERE id=%s",(id))
    # getthis=curser.fetchone()
    getthis=db.query(models.Post).filter(models.Post.id==id).first()
    
    if not getthis:# we can raise error in many ways first we will use response then http exception
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message":f"so the post you are loooking for with id {id} is not found"}so this is one way to use raise 404 now we will use better way 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"so the post you are loooking for with id {id} is not found")
    return getthis


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)# here we will delete posts with certain id
def delete_post(id:int,db: Session = Depends(get_db),username:str=Depends(oauth.get_current_user)):
    # curser.execute(" DELETE FROM info WHERE id=%s",(str(id)))# we have to convert id from int to str cause sql format is in string
    # conn.commit()
    # index_post=find_delete_post(id) we dont need this now 
    delete_post=db.query(models.Post).filter(models.Post.id==id)
    if  delete_post.first()==None:# if we did not found that post with certain id then we will return none in that case we raised extension 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"sorry this post with id {id} doesnt exist")
    
    if username.id!=delete_post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'you are not authorised for this action')
    
    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
# now we will update post

@router.put('/{id}',response_model=schemas.post)
def update_post(id:int,post:schemas.postupdate,db: Session = Depends(get_db),username:str=Depends(oauth.get_current_user)):
    # curser.execute("UPDATE info SET title=%s,content=%s,postable=%s WHERE id =%s returning *",(post.title,post.content,post.postable,id))
    # updated_post=curser.fetchone()
    # conn.commit()
    updated_post=db.query(models.Post).filter(models.Post.id==id).first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'the post you are looking for does not exist')
    
    if username.id!=updated_post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'you are not authorised for this action')
    for var,value in vars(post).items():
        setattr(updated_post,var,value)
    db.add(updated_post)

    db.commit()
    return updated_post
