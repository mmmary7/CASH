import os
import random
import sqlite3
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "cash.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. Добавляем 50 реалистичных клиентов
first_names = [
    "Александр",
    "Михаил",
    "Дмитрий",
    "Анна",
    "Елена",
    "Ольга",
    "Сергей",
    "Екатерина",
]
last_names = [
    "Смирнов",
    "Иванов",
    "Кузнецов",
    "Попов",
    "Васильев",
    "Петров",
    "Соколов",
]

for _ in range(50):
  name = f"{random.choice(last_names)} {random.choice(first_names)}"
  reg_date = (
      datetime(2026, 1, 1) + timedelta(days=random.randint(0, 250))
  ).strftime("%Y-%m-%d")
  cursor.execute(
      "INSERT INTO clients (full_name, registered_at) VALUES (?, ?)",
      (name, reg_date),
  )

# Получаем ID добавленных клиентов и категории
cursor.execute("SELECT client_id FROM clients")
client_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT category_id, cashback_percent FROM cashback_categories")
categories = cursor.fetchall()  # [(1, 1), (2, 5), (3, 7), (4, 5)]

# 2. Генерируем 1 500 транзакций за последние 6 месяцев
start_date = datetime(2026, 5, 1)

for _ in range(1500):
  c_id = random.choice(client_ids)
  cat_id, pct = random.choice(categories)
  # Чек от 150 до 15 000 руб
  amount = round(random.uniform(150, 15000), 2)
  cashback = round(amount * (pct / 100.0), 2)
  tx_time = start_date + timedelta(
      days=random.randint(0, 180),
      hours=random.randint(8, 22),
      minutes=random.randint(0, 59),
  )

  cursor.execute(
      """
        INSERT INTO transactions (client_id, category_id, amount, cashback_earned, transaction_date)
        VALUES (?, ?, ?, ?, ?)
    """,
      (c_id, cat_id, amount, cashback, tx_time.strftime("%Y-%m-%d %H:%M:%S")),
  )

conn.commit()
conn.close()
print("Сгенерировано 50 клиентов и 1500 транзакций!")