from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,Depends
from typing import Annotated
from app.data import fake_staff_db, password_hash
from app.models import StaffUser,StaffInDB
import jwt
from jwt import InvalidTokenError
from datetime import datetime ,timezone,timedelta
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY="6884b3837ce488319ea8320a8671dd1c188d0c5f13e992168d971449508b4146"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30


def get_current_staff(token:Annotated[str,Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        raise credentials_exception
    username = payload.get("sub")
    if username is None:
        raise credentials_exception
    user_dict = fake_staff_db.get(username)
    if user_dict is None:
        raise credentials_exception
    return StaffInDB(**user_dict)
                        
def get_current_active_user(current:Annotated[StaffUser,Depends(get_current_staff)]):
    if current.disabled:
         raise HTTPException(status_code=400,detail="inactive staff")
    return  current
def create_access_token(data:dict,expires_delta:timedelta):
    to_encode=data.copy()
    to_encode["exp"]=datetime.now(timezone.utc) + expires_delta
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)