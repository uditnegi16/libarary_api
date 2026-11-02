from fastapi import UploadFile,File,Form,APIRouter
from typing import Annotated

router=APIRouter(prefix="/covers",tags=["covers"])

@router.post("/upload")
def cover_upload(file:UploadFile):
    return {"file_name":file.filename,"content_type":file.content_type}

@router.post("/raw")
def covers_raw(file:Annotated[bytes,File()]):
    return {"size":len(file)}
@router.post("/titled")
def covers_titled(file:UploadFile,title:Annotated[str,Form()]):
    return{"title":title,"file_name":file.filename}