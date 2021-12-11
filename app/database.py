# first thing we did is we activate the virtual environment and set virtual env in terminak
#as well by passing venv\scripts\activate.bat in command line 

from fastapi import FastAPI 

#import psycopg2 # driver that will connect our python code to postgresql database
#from psycopg2.extras import RealDictCursor# this is for importing columns name in database becoz default coulmns names doesnt get printed



from app.router import auth 
from . import models,votes
from .orm import engine
from .router import posts,users,auth



models.Base.metadata.create_all(bind=engine)# i dont know what it does just paste it

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




app=FastAPI()#instance of fastapi

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(votes.router)










    





















