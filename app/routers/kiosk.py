from app.models import KioskCookies,KioskHeaders,KioskPing
from typing import Annotated
from fastapi  import Header, Cookie,APIRouter

router=APIRouter(prefix="/kiosk",tags=["kiosk"])


@router.get("/ping",response_model=KioskPing)
def ping_kiosk(
    cookies:Annotated[KioskCookies,Cookie()],
    headers:Annotated[KioskHeaders,Header()]
    ):
    return {
        "kiosk_id":"kiosk-1",
        "status":"ok",
        "session_token":cookies.session_token,
    }