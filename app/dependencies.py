from app.security import password_hash
from app.models import BorrowerInDB,BorrowerIn
def common_pagination(skip: int=0,limit:int=10):
    return {"skip":skip,"limit":limit}
def  write_log(message:str):
  with open("log.txt","a") as f:
      f.write(f"{message}\n")
      
def save_borrower(borrower_in:BorrowerIn)->BorrowerInDB:
   hashed=password_hash.hash(borrower_in.password)
   return BorrowerInDB(**borrower_in.model_dump(exclude={"password"}),hashed_password=hashed)