from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from services.plan_service import insert_plans

router = APIRouter(prefix="/plans", tags=["Plans"])

@router.post("/plans_insert")
def plans_insert(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return insert_plans(file, db)
