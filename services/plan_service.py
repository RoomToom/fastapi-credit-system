import pandas as pd
from sqlalchemy.orm import Session
from models import Plan, Dictionary

def insert_plans(file, db: Session):
    """
    Імпорт фінансових планів з Excel-файлу.

    :param file: Завантажений Excel-файл.
    :param db: Сесія бази даних.
    :return: Повідомлення про результат імпорту.
    """
    df = pd.read_excel(file.file)

    # Перевірка правильності колонок
    required_columns = {"period", "category_id", "sum"}
    if not required_columns.issubset(df.columns):
        return {"error": "Missing required columns"}

    df["period"] = pd.to_datetime(df["period"], errors="coerce")

    # Перевірка, що це перше число місяця
    if df["period"].isna().any() or (df["period"].dt.day != 1).any():
        return {"error": "Invalid period values"}

    # Перевірка, що сума не порожня
    if df["sum"].isna().any():
        return {"error": "Sum column contains empty values"}

    for _, row in df.iterrows():
        category = db.query(Dictionary).filter(Dictionary.id == row["category_id"]).first()
        if not category:
            return {"error": f"Category ID {row['category_id']} not found"}

        existing_plan = db.query(Plan).filter(
            Plan.period == row["period"], Plan.category_id == row["category_id"]
        ).first()
        if existing_plan:
            return {"error": "Plan for this period and category already exists"}

        new_plan = Plan(period=row["period"], sum=row["sum"], category_id=row["category_id"])
        db.add(new_plan)

    db.commit()
    return {"message": "Plans successfully inserted"}
