from fastapi import Depends,Query,Path,Body,HTTPException,APIRouter
from typing import Annotated
from app.data import fake_loans_db
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from datetime import timedelta,datetime
from app.models import Borrower,BorrowerIn,Loan,LoanTerms,LoanUpdate
from app.dependencies import common_pagination


router=APIRouter(prefix="/loans",tags=["loans"])
@router.get("/")
def show_all_loans(pagination:Annotated[dict,Depends(common_pagination)]):
    skip=pagination["skip"]
    limit=pagination["limit"]
    return list(fake_loans_db.values())[skip:skip+limit]


@router.get("/{loan_id}/due")
def get_due_loan_id(
    loan_id:Annotated[UUID,Path()],
    start:Annotated[datetime,Query()],
    period:Annotated[timedelta|None,Query()]=None):
    result={"loan_id":loan_id,"start":start}
    if period is not None:
        result["due"]=start+period
    return result

@router.put("/{loan_id}")
def put_body(loan_id:str,loan:Annotated[Loan,Body()]):
    fake_loans_db[loan_id]=jsonable_encoder(loan)
    return fake_loans_db[loan_id]

@router.patch("/{loan_id}")
def loan_update(loan_id:str,changes:Annotated[LoanUpdate,Body()]):
    if loan_id not in fake_loans_db:
        raise HTTPException(status_code=404,detail="loan id not found")

    stored_loan=Loan(**fake_loans_db[loan_id])
    update_data=changes.model_dump(exclude_unset=True)
    updated_loan=stored_loan.model_copy(update=update_data)
    fake_loans_db[loan_id]=jsonable_encoder(updated_loan)
    return fake_loans_db[loan_id]
