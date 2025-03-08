from sqlalchemy.orm import Session
from sqlalchemy.sql import func, case, and_
from models import Plan, Payment, Credit, Dictionary

def get_year_performance(year: int, db: Session):
    """
    Отримує аналітику виконання фінансових планів за певний рік.

    :param year: Рік для аналізу.
    :param db: Сесія бази даних.
    :return: Список зведених даних по місяцях.
    """
    results = (
        db.query(
            func.year(Plan.period).label("year"),
            func.month(Plan.period).label("month"),
            func.count(Credit.id).label("credits_count"),
            func.sum(case((Dictionary.name == "Видача", Plan.sum), else_=0)).label("planned_issuance"),
            func.sum(case((Dictionary.name == "Збір", Plan.sum), else_=0)).label("planned_collection"),
            func.sum(Credit.body).label("actual_issuance"),
            func.count(Payment.id).label("payments_count"),
            func.sum(Payment.sum).label("actual_collection")
        )
        .join(Dictionary, Plan.category_id == Dictionary.id)
        .outerjoin(Credit, and_(func.year(Credit.issuance_date) == year, Credit.id.isnot(None)))
        .outerjoin(Payment, and_(func.year(Payment.payment_date) == year, Payment.credit_id == Credit.id))
        .filter(func.year(Plan.period) == year)  # Фільтр тільки за потрібним роком
        .group_by(func.year(Plan.period), func.month(Plan.period))
        .all()
    )

    total_issuance = sum(row.actual_issuance or 0 for row in results)
    total_collection = sum(row.actual_collection or 0 for row in results)

    return [
        {
            "year": row.year,
            "month": row.month,
            "credits_count": row.credits_count,
            "planned_issuance": row.planned_issuance,
            "actual_issuance": row.actual_issuance,
            "issuance_percent": (row.actual_issuance / row.planned_issuance * 100) if row.planned_issuance else 0,
            "payments_count": row.payments_count,
            "planned_collection": row.planned_collection,
            "actual_collection": row.actual_collection,
            "collection_percent": (row.actual_collection / row.planned_collection * 100) if row.planned_collection else 0
        }
        for row in results
    ]

def get_plans_performance(date: str, db: Session):
    """
    Отримує інформацію про виконання фінансових планів на вказану дату.

    :param date: Дата у форматі 'YYYY-MM-DD'.
    :param db: Сесія бази даних.
    :return: Список даних про виконання планів.
    """
    date_parsed = func.date(date)

    results = (
        db.query(
            Plan.period, Dictionary.name, Plan.sum,
            func.coalesce(func.sum(Payment.sum), 0).label("actual_sum")
        )
        .join(Dictionary, Plan.category_id == Dictionary.id)
        .outerjoin(Payment, (Payment.payment_date <= date_parsed) & (Payment.type_id == Dictionary.id))
        .filter(Plan.period == date_parsed)
        .group_by(Plan.period, Dictionary.name, Plan.sum)
        .all()
    )

    return [
        {
            "period": str(period),
            "category": category,
            "planned_sum": plan_sum,
            "actual_sum": actual_sum,
            "performance_percent": (actual_sum / plan_sum) * 100 if plan_sum else 0
        }
        for period, category, plan_sum, actual_sum in results
    ]
