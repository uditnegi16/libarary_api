from app.models import BorrowerOut,BorrowerIn
from fastapi import BackgroundTasks,APIRouter
from app.dependencies import write_log,save_borrower

router=APIRouter(prefix="/borrowers",tags=["borrowers"])
@router.post("/register",response_model=BorrowerOut,status_code=201)
def registration(details:BorrowerIn,backgroundtaks:BackgroundTasks):
    backgroundtaks.add_task(write_log,f"registered {details.name}")
    return save_borrower(details)