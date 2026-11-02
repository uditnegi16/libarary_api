from fastapi import FastAPI,Path,Query,Body,Cookie,Header, Depends,Request,HTTPException,BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi import Form, File ,UploadFile,HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from uuid import UUID
from datetime import timedelta, datetime
from app.models import (
    BookSuggestion, Borrower, LoanTerms, BookFilter,
    KioskCookies, KioskHeaders, KioskPing,
    BorrowerIn, BorrowerOut, BorrowerInDB,
    Loan, LoanUpdate, StaffUser, StaffInDB,
    BookNotAvailableError,
)

from app.data import fake_loans_db,fake_books,fake_staff_db
from fastapi.staticfiles import StaticFiles
from app.security import create_access_token,get_current_active_user,ACCESS_TOKEN_EXPIRE_MINUTES,password_hash
import time 



from app.routers import loans,books,borrowers,staff,covers,kiosk,auth

tags_metadata = [
    {"name": "books", "description": "Look up, search and suggest books."},
    {"name": "staff", "description": "Staff login and the current staff user."},
    {"name": "borrowers", "description": "Register borrowers."},
    {"name": "kiosk", "description": "Check-in kiosk status."},
]

app = FastAPI(
    title="Library API",
    description="A small library system: books, loans, borrowers and staff login.",
    summary="Practice library backend",
    version="1.0.0",
    openapi_tags=tags_metadata,
)
app.mount("/static", StaticFiles(directory="static"), name="static")
origins=["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(CORSMiddleware,allow_origins=origins, allow_credentials=True,allow_headers=["*"],allow_methods=["*"])

app.include_router(loans.router)
app.include_router(books.router)
app.include_router(borrowers.router)
app.include_router(covers.router)
app.include_router(kiosk.router)
app.include_router(staff.router)
app.include_router(auth.router)


@app.middleware("http")
async def count_process_time(request:Request,call_next):
    start_time=time.perf_counter()
    response=await call_next(request)
    process_time=time.perf_counter()-start_time
    response.headers["X-Process-Time"]=str(process_time)
    return response    


@app.post("/loan")
def loan(borrower:Borrower,loanterms:LoanTerms,notes:Annotated[str|None,Body()]=None):
    return {"borrower":borrower.model_dump(),"loanterms":loanterms.model_dump(),"notes":notes}



@app.exception_handler(BookNotAvailableError)
async def book_not_available_handler(request:Request,exc:BookNotAvailableError):
    return JSONResponse(status_code=409,content={"details":f"{exc.title} is not available"})

        
