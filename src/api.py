import os
import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="CASH API Service", version="1.0")

# Путь к нашей локальной базе данных
DB_PATH = os.path.join(os.path.dirname(__file__), "database", "cash.db")


# Формат входящего JSON-запроса (Контракт Request)
class CashbackRequest(BaseModel):
  client_id: int
  category_id: int
  amount: float


# Формат исходящего JSON-ответа (Контракт Response)
class CashbackResponse(BaseModel):
  status: str
  client_name: str
  category_name: str
  cashback_percent: int
  cashback_amount: float

# Главная страница 
@app.get("/")
def read_root():
  return {
      "message": "CASH API работает штатно!",
      "docs_url": "http://127.0.0.1:8000/docs",
  }

# Сам эндпоинт расчета кешбэка
@app.post("/api/v1/cashback/calculate", response_model=CashbackResponse)
def calculate_cashback(req: CashbackRequest):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()

  # Проверяем, существует ли такой клиент
  cursor.execute(
      "SELECT full_name FROM clients WHERE client_id = ?", (req.client_id,)
  )
  client = cursor.fetchone()
  if not client:
    conn.close()
    raise HTTPException(status_code=404, detail="Клиент не найден")

  # Проверяем категорию и процент бонуса
  cursor.execute(
      "SELECT category_name, cashback_percent FROM cashback_categories WHERE"
      " category_id = ?",
      (req.category_id,),
  )
  category = cursor.fetchone()
  if not category:
    conn.close()
    raise HTTPException(status_code=404, detail="Категория не найдена")

  conn.close()

  # Бизнес-логика: расчет суммы бонуса
  client_name = client[0]
  cat_name, percent = category[0], category[1]
  cashback_val = round(req.amount * (percent / 100.0), 2)

  return CashbackResponse(
      status="APPROVED",
      client_name=client_name,
      category_name=cat_name,
      cashback_percent=percent,
      cashback_amount=cashback_val,
  )