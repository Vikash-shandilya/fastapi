from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")# used for choosing algo rithm for hashing in this case its bcrypt
def makehash(password:str):
    hashed_password=pwd_context.hash(password)
    return hashed_password

def verify_password(plain_pass,hashed_pass):# it verify the password given  user by checking into database 
    return pwd_context.verify(plain_pass,hashed_pass)# this line convert plain_pass to hashed pass and then it matched with alredy
                                                    #hashed pass in our database . 
