-- Таблица клиентов
CREATE TABLE IF NOT EXISTS clients (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    registered_at DATE NOT NULL
);

-- Таблица категорий повышенного кешбэка
CREATE TABLE IF NOT EXISTS cashback_categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL,
    cashback_percent INTEGER NOT NULL
);

-- Таблица транзакций
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER REFERENCES clients(client_id),
    category_id INTEGER REFERENCES cashback_categories(category_id),
    amount REAL NOT NULL,
    cashback_earned REAL NOT NULL,
    transaction_date TEXT NOT NULL
);