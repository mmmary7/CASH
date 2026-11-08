-- 1. Маржинальность и расходы банка по категориям
-- Показывает объем выплат и долю кешбэка от общего оборота трат
SELECT 
    c.category_name,
    COUNT(t.transaction_id) AS total_transactions,
    ROUND(SUM(t.amount), 2) AS total_turnover,
    ROUND(SUM(t.cashback_earned), 2) AS total_cashback_paid,
    ROUND((SUM(t.cashback_earned) / SUM(t.amount)) * 100, 2) AS effective_cashback_rate_pct
FROM transactions t
JOIN cashback_categories c ON t.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total_cashback_paid DESC;

-- 2. Клиентский срез: активность и средний чек
-- Анализ распределения бонусов по конкретным пользователям
SELECT 
    cl.client_id,
    cl.full_name,
    COUNT(t.transaction_id) AS transactions_count,
    ROUND(AVG(t.amount), 2) AS avg_receipt,
    ROUND(SUM(t.amount), 2) AS total_spent,
    ROUND(SUM(t.cashback_earned), 2) AS total_cashback_received
FROM clients cl
LEFT JOIN transactions t ON cl.client_id = t.client_id
GROUP BY cl.client_id, cl.full_name
ORDER BY total_cashback_received DESC;

-- 3. Оконная функция: ранжирование покупок клиента по сумме кешбэка
-- Выделяет топ-транзакции внутри каждого клиента
SELECT 
    cl.full_name,
    c.category_name,
    t.amount,
    t.cashback_earned,
    DENSE_RANK() OVER (PARTITION BY cl.client_id ORDER BY t.cashback_earned DESC) AS rank_by_cashback
FROM transactions t
JOIN clients cl ON t.client_id = cl.client_id
JOIN cashback_categories c ON t.category_id = c.category_id;