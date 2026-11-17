
-- 1. Проверка качества данных (Data Quality)
-- Сверка уникальности ключей и поиск операций без привязки к категории

SELECT 
    COUNT(transaction_id) AS total_rows,
    COUNT(DISTINCT transaction_id) AS unique_transactions,
    SUM(CASE WHEN amount <= 0 OR amount IS NULL THEN 1 ELSE 0 END) AS invalid_amounts
FROM transactions;


-- 2. Маржинальность категорий (INNER JOIN + GROUP BY + HAVING)
-- Выводим категории с оборотом выше 10 000 руб. и считаем долю выплат

SELECT 
    c.category_name,
    COUNT(t.transaction_id) AS tx_count,
    ROUND(SUM(t.amount), 2) AS total_turnover,
    ROUND(SUM(t.cashback_earned), 2) AS total_cashback_paid,
    ROUND((SUM(t.cashback_earned) / SUM(t.amount)) * 100, 2) AS effective_rate_pct
FROM transactions t
INNER JOIN cashback_categories c ON t.category_id = c.category_id
GROUP BY c.category_name
HAVING SUM(t.amount) > 10000
ORDER BY total_cashback_paid DESC;

-- 3. Сегментация клиентов (LEFT JOIN + COALESCE + CASE WHEN)
-- Учитываем даже «спящих» клиентов без транзакций (заменяем NULL на 0)

SELECT 
    cl.client_id,
    cl.full_name,
    COUNT(t.transaction_id) AS tx_count,
    ROUND(COALESCE(AVG(t.amount), 0), 2) AS avg_receipt,
    ROUND(COALESCE(SUM(t.cashback_earned), 0), 2) AS total_cashback,
    CASE 
        WHEN COALESCE(SUM(t.amount), 0) >= 50000 THEN 'VIP'
        WHEN COALESCE(SUM(t.amount), 0) > 0 THEN 'Active'
        ELSE 'Inactive'
    END AS client_segment
FROM clients cl
LEFT JOIN transactions t ON cl.client_id = t.client_id
GROUP BY cl.client_id, cl.full_name
ORDER BY total_cashback DESC;


-- 4. Оконные функции (ROW_NUMBER и DENSE_RANK)
-- Ранжирование покупок внутри каждого клиента по сумме кешбэка

SELECT 
    cl.full_name,
    c.category_name,
    t.amount,
    t.cashback_earned,
    ROW_NUMBER() OVER (PARTITION BY cl.client_id ORDER BY t.transaction_date DESC) AS tx_chronological_num,
    DENSE_RANK() OVER (PARTITION BY cl.client_id ORDER BY t.cashback_earned DESC) AS cashback_rank
FROM transactions t
INNER JOIN clients cl ON t.client_id = cl.client_id
INNER JOIN cashback_categories c ON t.category_id = c.category_id;