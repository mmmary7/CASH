import os
import sqlite3

# Путь к текущей директории скрипта (src/database/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "cash.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Читаем и выполняем schema.sql
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
  cursor.executescript(f.read())

# Наполняем тестовыми данными
cursor.executescript("""
INSERT INTO clients (full_name, registered_at) VALUES 
('Иванов И.И.', '2026-01-15'),
('Петров П.П.', '2026-02-10'),
('Сидорова А.В.', '2026-03-01');

INSERT INTO cashback_categories (category_name, cashback_percent) VALUES 
('Супермаркеты', 1),
('Рестораны и кафе', 5),
('Аптеки', 7),
('АЗС', 5);

INSERT INTO transactions (client_id, category_id, amount, cashback_earned, transaction_date) VALUES 
(1, 1, 3500.00, 35.00, '2026-11-01 10:30:00'),
(1, 2, 2400.00, 120.00, '2026-11-02 19:45:00'),
(2, 3, 1500.00, 105.00, '2026-11-03 14:15:00'),
(3, 4, 4000.00, 200.00, '2026-11-04 09:00:00'),
(1, 3, 900.00, 63.00, '2026-11-04 18:20:00');
""")

conn.commit()
conn.close()
print(f"База успешно создана: {DB_PATH}")