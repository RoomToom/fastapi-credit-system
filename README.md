# 📌 FastAPI Credit System

This project implements a **REST API** for managing credits, plans, and payments using **FastAPI**, **SQLAlchemy**, and **MySQL**.  
The API allows users to retrieve credit information, upload financial plans, and analyze their execution.

## **📌 Key Endpoints**
🔹 **`GET /user_credits/{user_id}`** – Retrieve user credit information  
🔹 **`POST /plans_insert`** – Upload financial plans from Excel  
🔹 **`GET /plans_performance?date=YYYY-MM-DD`** – Get plan performance for a specific date  
🔹 **`GET /year_performance?year=YYYY`** – Annual financial analytics  

---

## **📌 Cloning the Repository**
To download this project, run:
```bash
git clone https://github.com/RoomToom/fastapi-credit-system.git
cd fastapi-credit-system
```

---

## **📌 Installing Dependencies**
Before running the project, install all required packages:
```bash
pip install -r requirements.txt
```
---

## **📌 Database Setup**
This project uses **MySQL**, and all necessary files for importing test data are located in the `data/` folder.

### 1️⃣ **Create the `test_db` database**
```sql
CREATE DATABASE test_db;
```

### 2️⃣ **Import `test_db_dump.sql` into `test_db`**
The file `data/test_db_dump.sql` contains all the provided test data required for the API to function. To import it, run:
```bash
mysql -u root -p test_db < data/test_db_dump.sql
```

---

## **📌 Configuring `.env`**
The **`.env` file contains sensitive data**, so it is **not included in the repository**.  
To correctly configure database connection settings, follow these steps:

1️⃣ **Create a `.env` file in the project root**  
2️⃣ **Fill it in based on `env.example`**  
```ini
DATABASE_URL=mysql+mysqlconnector://root:yourpassword@localhost:3306/test_db
```

---

## **📌 Running FastAPI**
After setting up the database, start the FastAPI server:
```bash
uvicorn main:app --reload
```
---

## **📌 API Documentation**
FastAPI automatically generates **Swagger UI** documentation.  
Open in your browser: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

## **📌 Test Files**
The `data/` folder contains files for testing the API:
1. **`test_db_dump.sql`** – Database with test records.  
2. **`plans.xlsx`** – Sample Excel file for testing `/plans_insert`.  

---
