from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from models import Credit, Payment
from datetime import date
from fastapi import HTTPException

def get_user_credits(user_id: int, db: Session):
    """
    Отримує інформацію про кредити користувача.

    :param user_id: ID користувача.
    :param db: Сесія бази даних.
    :return: Список кредитів користувача або повідомлення, якщо їх немає.
    """
    credits = db.query(
        Credit.id, Credit.issuance_date, Credit.return_date, Credit.actual_return_date,
        Credit.body, Credit.percent,
        func.coalesce(func.sum(Payment.sum), 0).label("total_payments")
    ).outerjoin(Payment, Payment.credit_id == Credit.id).filter(Credit.user_id == user_id).group_by(Credit.id).all()

    # Якщо у користувача немає кредитів – повертаємо повідомлення
    if not credits:
        raise HTTPException(status_code=404, detail="У користувача немає записів про кредити.")

    result = []
    for credit in credits:
        credit_status = credit.actual_return_date is not None  # True = закритий, False = відкритий
        data = {
            "issuance_date": credit.issuance_date,
            "closed": credit_status
        }

        if credit_status:
            data.update({
                "return_date": credit.actual_return_date,
                "body": credit.body,
                "percent": credit.percent,
                "total_payments": credit.total_payments
            })
        else:
            #Перетворюємо `return_date` у Python `date`
            if credit.return_date:
                overdue_days = (credit.return_date - date.today()).days
                overdue_days = max(overdue_days, 0)  # Не допускаємо від'ємних значень
            else:
                overdue_days = 0  # Якщо `return_date` немає, прострочки немає

            # Отримуємо окремі платежі по тілу та відсоткам
            payments_body = db.query(func.coalesce(func.sum(Payment.sum), 0)).filter(
                Payment.credit_id == credit.id, Payment.type_id == 1  # 1 = платежі по тілу (припущення)
            ).scalar()

            payments_percent = db.query(func.coalesce(func.sum(Payment.sum), 0)).filter(
                Payment.credit_id == credit.id, Payment.type_id == 2  # 2 = платежі по відсоткам (припущення)
            ).scalar()

            data.update({
                "return_date": credit.return_date,
                "overdue_days": overdue_days,
                "body": credit.body,
                "percent": credit.percent,
                "total_payments_body": payments_body,
                "total_payments_percent": payments_percent
            })

        result.append(data)

    return result
