import os
import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="CASH Analytics Dashboard", layout="wide")
st.title("💳 CASH — Мониторинг программы лояльности")

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "cash.db")
conn = sqlite3.connect(DB_PATH)

# Загрузка аналитических срезов
df_tx = pd.read_sql_query(
    """
    SELECT 
        c.category_name,
        t.amount,
        t.cashback_earned,
        DATE(t.transaction_date) as tx_date
    FROM transactions t
    JOIN cashback_categories c ON t.category_id = c.category_id
""",
    conn,
)

conn.close()

# 1. Верхние KPI метрики
col1, col2, col3 = st.columns(3)
col1.metric("Суммарный оборот трат", f"{df_tx['amount'].sum():,.2f} ₽")
col2.metric("Выплачено кешбэка", f"{df_tx['cashback_earned'].sum():,.2f} ₽")
effective_rate = (
    df_tx["cashback_earned"].sum() / df_tx["amount"].sum()
) * 100
col3.metric("Эффективная ставка банка", f"{effective_rate:.2f} %")

st.divider()

# 2. Графики
col_left, col_right = st.columns(2)

with col_left:
  st.subheader("Выплаты кешбэка по категориям")
  cat_summary = (
      df_tx.groupby("category_name")["cashback_earned"].sum().reset_index()
  )
  st.bar_chart(
      data=cat_summary, x="category_name", y="cashback_earned", color="#FFDD2D"
  )

with col_right:
  st.subheader("Топ категорий по обороту")
  cat_turnover = df_tx.groupby("category_name")["amount"].sum().reset_index()
  st.bar_chart(data=cat_turnover, x="category_name", y="amount")