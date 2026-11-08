-- 1. Топ категорий по суммарным выплатам кешбэка
SELECT 
    c.category_name,
    COUNT(t.transaction_id) AS tx_count,
    ROUND(SUM(t.amount), 2) AS total_spent,
    ROUND(SUM(t.cashback_earned), 2) AS total_cashback
FROM transactions t
JOIN cashback_categories c ON t.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total_cashback DESC;

-- 2. Клиентский срез: средний чек и накопленный кешбэк
SELECT 
    cl.client_id,
    cl.full_name,
    COUNT(t.transaction_id) AS transactions_count,
    ROUND(AVG(t.amount), 2) AS avg_ticket,
    ROUND(SUM(t.cashback_earned), 2) AS total_cashback
FROM clients cl
JOIN transactions t ON cl.client_id = t.client_id
GROUP BY cl.client_id, cl.full_name;