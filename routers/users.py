from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.user_service import get_user_credits

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/user_credits/{user_id}")
def user_credits(user_id: int, db: Session = Depends(get_db)):
    return get_user_credits(user_id, db)
