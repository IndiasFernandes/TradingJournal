import sqlite3
from datetime import datetime, timedelta

DATABASE_FILE = "trading_journal.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Trade (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            side TEXT,
            entry_price REAL,
            leverage INTEGER,
            time_open TEXT,
            state TEXT,
            buy_orders_ids TEXT,
            stop_loss_orders_ids TEXT,
            max_risk REAL,
            trigger_safe_stop_loss REAL,
            amount_safe_stop_loss REAL,
            percentage REAL,
            pnl REAL,
            other_variables TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TradeDay (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            total_trades INTEGER,
            avg_pnl REAL,
            total_pnl REAL,
            other_variables TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Account (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            account_balance REAL,
            real_account_balance REAL,
            margin_ratio REAL,
            other_variables TEXT
        )
    ''')

    conn.commit()
    conn.close()

setup_database()