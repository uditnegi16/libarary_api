from typing import Annotated
from fastapi import Form,Depends,APIRouter
from app.models import StaffUser
from app.security import get_current_active_user

router=APIRouter(prefix="/staff",tags=["staff"])
@router.post("/login")
def staff_login(username:Annotated[str,Form()],password:Annotated[str,Form()]):
    return {"username":username}

@router.get("/me",response_model=StaffUser)
def get_token(
    current_staff:Annotated[StaffUser,Depends(get_current_active_user)]):
    return current_staff