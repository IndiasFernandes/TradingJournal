import sqlite3
from datetime import datetime, timedelta

DATABASE_FILE = "trading_journal.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def insert_dummy_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")

        # Insert 4 trades per day
        for j in range(4):
            cursor.execute('''
                INSERT INTO Trade (symbol, side, entry_price, leverage, time_open, state, max_risk, trigger_safe_stop_loss, amount_safe_stop_loss, percentage, pnl)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', ('AAPL', 'Long', 150 + j, 2, date_str, 'Open', 0.1, 0.05, 0.1, 0.2, 50))

        # Insert TradeDay summary
        cursor.execute('''
            INSERT INTO TradeDay (date, total_trades, avg_pnl, total_pnl, other_variables)
            VALUES (?, ?, ?, ?, ?)
        ''', (date_str, 4, 0.05, 0.2, 'variable'))

        # Insert Account data
        cursor.execute('''
            INSERT INTO Account (datetime, account_balance, real_account_balance, margin_ratio, other_variables)
            VALUES (?, ?, ?, ?, ?)
        ''', (date_str, 10000, 9500, 0.25, 'variable'))

    conn.commit()
    conn.close()

insert_dummy_data()