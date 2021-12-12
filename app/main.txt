# # first thing we did is we activate the virtual environment and set virtual env in terminak
# #as well by passing venv\scripts\activate.bat in command line 
# from typing import Optional
# from fastapi import FastAPI , status,Response,HTTPException
# from fastapi.params import Body
# from pydantic import BaseModel
# from random import randrange
# import psycopg2 # driver that will connect our python code to postgresql database
# from psycopg2.extras import RealDictCursor# this is for importing columns name in database becoz default coulmns names doesnt get printed
# import time 

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='$@91Dimple',
#         cursor_factory=RealDictCursor)#  Connect to your postgres DB
#         curser=conn.cursor()# Open a cursor to perform database operations
#         print('database connection succesfull')
#         break

#     except Exception as errors:
#         print('database connection unsuccesfull')
#         print('errors :',errors )
#         time.sleep(3)



# class post(BaseModel):# this class is actually used for validation in our post 
#     title:str# this is inherited from pydantic basemodel and used for validation
#     content:str
#     postable:bool=True
#     #rating:Optional[int]=None# so this is actually used to make option that means
#     #if i want to post or not post in both case it should be ok but you have to import it 

# app=FastAPI()#instance of fastapi

# my_post=[{"title":"this is post1 title","content":"this is post 1 content","postable": False,"rating":5,"id":3}
# ,{"title":"this is post2 title","content":"this is post 2 content","postable": True,"rating":4,"id":2}]



# @app.get("/")
# def root():
#     return {"message": "to view post go to /posts url"}

# @app.get("/posts")
# def get_posts():
#     curser.execute(" SELECT * FROM info")
#     post=curser.fetchall()
#     return {'posts': post}

# @app.post("/createpost",status_code=status.HTTP_201_CREATED)# we changed the status code 200 to 201 because whenever post is created 201 statuscode should be sent a/q documentation
# def create(new_post:post):# here we cretaed a variable new_post and assign it to our class post we put parameter new_post:post this will validate whtaever we inpu using front end or postman(through body and raw)
#     # print(new_post)#so now everything will be done by this class only actually there is one method
#     # #new_post.dict() this will convert our pydantic model into dictionary
#     # new_dict=new_post.dict()
#     # new_dict['id']=randrange(1,1000000000)# used for creating and  assigning a unique id 
#     # my_post.append(new_dict)
#     # we will now use database so code that is above is not very useful . so i will comment it out
#     curser.execute("INSERT INTO info(title,content,postable) VALUES(%s,%s,%s)RETURNING *",(new_post.title,new_post.content,new_post.postable))# so this is used for inserting input into database by frontend
#     cretaed_post=curser.fetchone()# this is used to return one post that is created obviously one more thing to fetch the post we have to first return that
#     conn.commit()# to save changes into database we have to acually commit 
#     return {"message":f"{cretaed_post}"}

# def findpost(id):# this function is for searching if post exists with given id
#     for p in my_post:
#         if p['id']==id:
#             return p

# # @app.get("/posts/latest") we do not need this this is just for you to understand
# # def get_latest():
# #     post=my_post[len(my_post)-1]
# #     return {'latest_post':post}



# @app.get("/posts/{id}")# this is for getting specific posts 
# def get_post(id,response:Response):#
    
#     getthis=findpost(int(id))
#     if not getthis:# we can raise error in many ways first we will use response then http exception
#         # response.status_code=status.HTTP_404_NOT_FOUND
#         # return {"message":f"so the post you are loooking for with id {id} is not found"}so this is one way to use raise 404 now we will use better way 
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"so the post you are loooking for with id {id} is not found")
#     return {"post_that you asked for":getthis}


# # @app.get("/posts/latest")
# # def get_latest():
# #     post=my_post[len(my_post)-1]
# #     return {'latest_post':post}# you can see if we run this code it will throw error becuase see above code
#     #their url path and when we put /post/latest it get matches with their url path and throws error cause
#     #latest is not an integer so what will we do we will put the whole code above 

# # now lets delete something
# def find_delete_post(id):# if found return index of post which contain this {id}
#     for i,p in enumerate(my_post):
#         if id==p['id']:
#             return i# returns index of that id

# @app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)# here we will delete posts with certain id
# def delete_post(id:int):
#     curser.execute(" DELETE FROM info WHERE id=%s",(id))
#     deleted_post=curser.fetchone()
#     # index_post=find_delete_post(id) we dont need this
#     if  index_post==None:# if we did not found that post with certain id then we will return none in that case we raised extension 404
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"sorry this post with id {id} doesnt exist")
#     my_post.pop(index_post)# delete post by that index name

# # now we will update post

# @app.put('/posts/{id}')
# def update_post(id:int,post:post):
#     getthis=find_delete_post(id)# to find the index of my post
#     if getthis==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'the post you are looking for does not exist')
#     postdict=post.dict()# as my data is in json format so and data in my_post is in dict format so will convert json to dict
#     postdict['id']=id# we will assign the same id to new dict 
    
#     my_post[getthis]=postdict# we will now replace previous post with postdict
#     return my_post[getthis]

    





















