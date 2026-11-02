from typing import Annotated
from fastapi import Depends,HTTPException,Query,Path
from app.data import fake_books
from app.models import BookNotAvailableError,BookFilter,BookSuggestion
from fastapi import APIRouter
from app.dependencies import common_pagination
router=APIRouter(tags=["books"])
@router.get("/books/filter")
def filter_book(filters:Annotated[BookFilter,Query()],pagination: Annotated[dict, Depends(common_pagination)]):
     return {"filters": filters.model_dump(), "pagination": pagination}
 
 
@router.get("/books/{book_id}",summary="Get a book by ID",description="Returns the book if it exists and is available. Gives 404 if the ID is unknown and 409 if the book is currently checked out.")
def check_book_id(book_id:int):
    if book_id not in fake_books:## or if fake_books[book_id] is None:
        raise HTTPException(status_code=404,detail="book not found")
    if fake_books[book_id]["available"]:
        return fake_books[book_id]
    raise BookNotAvailableError(fake_books[book_id]["title"])

@router.get("/search",tags=["books"],deprecated=True)
def search_book(q:Annotated[str|None,Query(min_length=3,max_length=50)]=None):
    return {"q":q}
@router.get("/book/{book_id}",tags=["books"])
def give_book_id(book_id:Annotated[int,Path(title="the id of the  book",gt=0)],summary:bool=False):
    if summary:
        return {"book_id":book_id,"summary" : summary}
    return {"book_id" : book_id}

@router.post("/book/suggest",tags=["books"])
def suggestion(book_sug : BookSuggestion,urgent : bool=False):
    return {"suggestions":book_sug.model_dump(),"urgent":urgent}
@router.get("/books/{book_id}",tags=["books"],summary="Get a book by ID",description="Returns the book if it exists and is available. Gives 404 if the ID is unknown and 409 if the book is currently checked out.")
def check_book_id(book_id:int):
    if book_id not in fake_books:## or if fake_books[book_id] is None:
        raise HTTPException(status_code=404,detail="book not found")
    if fake_books[book_id]["available"]:
        return fake_books[book_id]
    raise BookNotAvailableError(fake_books[book_id]["title"])