# first thing we did is we activate the virtual environment and set virtual env in terminak
#as well by passing venv\scripts\activate.bat in command line 

from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware

#import psycopg2 # driver that will connect our python code to postgresql database
#from psycopg2.extras import RealDictCursor# this is for importing columns name in database becoz default coulmns names doesnt get printed



from app.router import auth 
from app import models,votes
from app.orm import engine
from app.router import posts,users,auth



#models.Base.metadata.create_all(bind=engine)# i dont know what it does just paste it

app=FastAPI()#instance of fastapi

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# while True:
#     try: we dont need this in ORM model so i have commented it out
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Vikash123',
#         cursor_factory=RealDictCursor)#  Connect to your postgres DB
#         curser=conn.cursor()# Open a cursor to perform database operations
#         print('database connection succesfull')
#         break

#     except Exception as errors:
#         print('database connection unsuccesfull')
#         print('errors :',errors )
#         time.sleep(3)






app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get('/')
def root():
    return {'result':'hello world'}







    





















