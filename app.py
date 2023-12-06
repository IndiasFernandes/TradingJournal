from flask import Flask, render_template, jsonify
import sqlite3
from datetime import datetime, timedelta

# Initialize Flask App
app = Flask(__name__)

# Database file
DATABASE_FILE = "trading_journal.db"

# Database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# Setup Database
def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Creating tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS Trade (
                          id INTEGER PRIMARY KEY,
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
                          pnl REAL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS TradeDay (
                          id INTEGER PRIMARY KEY,
                          date TEXT,
                          total_trades INTEGER,
                          avg_pnl REAL,
                          total_pnl REAL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Account (
                          id INTEGER PRIMARY KEY,
                          datetime TEXT,
                          account_balance REAL,
                          real_account_balance REAL,
                          margin_ratio REAL)''')

    conn.commit()
    conn.close()

# Insert Dummy Data
def insert_dummy_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")

        # Insert 4 trades per day
        for j in range(4):
            cursor.execute('''INSERT INTO Trade (symbol, side, entry_price, leverage, time_open, state, max_risk, ...)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ...)''',
                           ('AAPL', 'Long', 150 + j, 2, date_str, 'Open', 0.1, ...))

        # Insert TradeDay summary
        cursor.execute('''INSERT INTO TradeDay (date, total_trades, avg_pnl, total_pnl, ...)
                          VALUES (?, ?, ?, ?, ...)''',
                       (date_str, 4, 0.05, 0.2, ...))

        # Insert Account data
        cursor.execute('''INSERT INTO Account (datetime, account_balance, real_account_balance, margin_ratio, ...)
                          VALUES (?, ?, ?, ?, ...)''',
                       (date_str, 10000, 9500, 0.25, ...))

    conn.commit()
    conn.close()

# Route for homepage
@app.route('/')
def index():
    conn = get_db_connection()
    trades = conn.execute('SELECT * FROM Trade').fetchall()
    trade_days = conn.execute('SELECT * FROM TradeDay').fetchall()
    account_data = conn.execute('SELECT * FROM Account').fetchall()
    conn.close()

    return render_template('index.html', trades=trades, trade_days=trade_days, account_data=account_data)

# Start the Flask application
if __name__ == '__main__':
    setup_database()
    insert_dummy_data()
    app.run(debug=True)
