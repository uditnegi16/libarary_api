from pydantic import BaseModel,Field
from datetime import datetime
class BookNotAvailableError(Exception):
    def __init__(self,title):
        self.title=title
        
class Publisher(BaseModel):
    name:str
    country:str|None=None
    
class BookSuggestion(BaseModel):
    title:str
    author:str
    year:int|None=None
    publisher:Publisher|None=None
    genres:list[str]=[]
    pages:int=Field(gt=0,le=5000,description="Number of pages")
    
class Borrower(BaseModel):
    name:str
    email:str
class LoanTerms(BaseModel):
    due_in_days:int=Field(gt=0,le=90,description="Days until the book is due")
class BookFilter(BaseModel):
    genre:str|None=None
    author:str|None=None
    limit:int=Field(10,gt=0,le=100)

class KioskCookies(BaseModel):
    session_token:str|None=None
class KioskHeaders(BaseModel):
    app_version:str|None=None
class KioskPing(BaseModel):
    kiosk_id:str
    status:str
    
    
class BorrowerIn(BaseModel):
    name:str
    email:str
    password:str
class BorrowerOut(BaseModel):
    name:str
    email:str
class BorrowerInDB(BaseModel):
    name:str
    email:str
    hashed_password:str
    
class Loan(BaseModel):
    book_id:int
    borrower:str
    due:datetime
    notes:str| None = None
    
class LoanUpdate(BaseModel):
    borrower:str|None=None
    due:datetime|None=None
    notes:str|None=None
class StaffUser(BaseModel):
    username:str
    full_name:str|None=None
    disabled:bool|None=None
class StaffInDB(StaffUser):
    hashed_password:str