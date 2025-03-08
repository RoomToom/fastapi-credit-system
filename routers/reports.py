from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from services.report_service import get_year_performance, get_plans_performance

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/year_performance")
def year_performance(year: int, db: Session = Depends(get_db)):
    return get_year_performance(year, db)

@router.get("/plans_performance")
def plans_performance(
        date: str = Query(..., description="Дата у форматі YYYY-MM-DD (наприклад, 2020-01-01)"),
        db: Session = Depends(get_db)):
    return get_plans_performance(date, db)
