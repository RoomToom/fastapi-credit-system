# 📌 FastAPI Credit System

Цей проєкт реалізує **REST API** для роботи з кредитами, планами та платежами, використовуючи **FastAPI**, **SQLAlchemy** та **MySQL**.  
API дозволяє отримувати інформацію про кредити користувачів, завантажувати фінансові плани та аналізувати їх виконання.

## **📌 Основні ендпоінти**
🔹 **`GET /user_credits/{user_id}`** – Отримати інформацію про кредити користувача  
🔹 **`POST /plans_insert`** – Завантажити фінансові плани з Excel  
🔹 **`GET /plans_performance?date=YYYY-MM-DD`** – Виконання планів на дату  
🔹 **`GET /year_performance?year=YYYY`** – Аналітика по фінансах за рік  

---

## **📌 Клонування репозиторію**
Щоб завантажити цей проєкт, виконайте команду:
```bash
git clone https://github.com/RoomToom/fastapi-credit-system.git
cd fastapi-credit-system
```

---

## **📌 Встановлення залежностей**
Перед запуском проєкту потрібно встановити всі необхідні пакети:
```bash
pip install -r requirements.txt
```
---

## **📌 Налаштування бази даних**
Проєкт використовує **MySQL**, і в папці `data/` містяться всі необхідні файли для імпорту тестових даних.

### 1️⃣ **Створіть базу даних `test_db`**
```sql
CREATE DATABASE test_db;
```

### 2️⃣ **Імпортуйте `test_db_dump.sql` у `test_db`**
Файл `data/test_db_dump.sql` містить усі надані тестові дані, необхідні для роботи API. Щоб імпортувати його, виконайте:
```bash
mysql -u root -p test_db < data/test_db_dump.sql
```

---

## **📌 Налаштування `.env`**
**Файл `.env` містить конфіденційні дані**, тому він **не входить до репозиторію**.  
Щоб правильно налаштувати підключення до бази даних, виконайте наступне:

1️⃣ **Створіть `.env` у корені проєкту**  
2️⃣ **Заповніть його на основі `env.example`**  
```ini
DATABASE_URL=mysql+mysqlconnector://root:yourpassword@localhost:3306/test_db
```

---

## **📌 Запуск FastAPI**
Після налаштування бази даних запустіть сервер FastAPI:
```bash
uvicorn main:app --reload
```
---

## **📌 Документація API**
FastAPI автоматично створює документацію **Swagger UI**.  
Відкрийте в браузері: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

## **📌 Тестові файли**
У папці `data/` містяться файли для тестування API:
1. **`test_db_dump.sql`** – база даних із тестовими записами.  
2. **`plans.xlsx`** – тестовий Excel-файл для перевірки `/plans_insert`.  

---




