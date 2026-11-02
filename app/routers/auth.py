from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends,HTTPException,APIRouter
from app.data import fake_staff_db,password_hash
from app.models import StaffInDB

from app.security import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router=APIRouter(tags=["auth"])
@router.post("/token")
def first_login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
   user_dict=fake_staff_db.get(form_data.username)
   if user_dict is None:
       raise HTTPException(status_code=400,detail="Incorrect username or password")
   user=StaffInDB(**user_dict)
   if not password_hash.verify(form_data.password, user.hashed_password):
       raise HTTPException(status_code=400, detail="Incorrect username or password")
   data={"sub":user.username}
   access_token=create_access_token(data,expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
   return {"access_token": access_token,"token_type":"bearer"}