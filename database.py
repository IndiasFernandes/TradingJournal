import sqlite3
from datetime import datetime, timedelta

DATABASE_FILE = "trading_journal.db"

def get_db_connection():
    """
    Create and return a connection to the SQLite database.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    """
    Set up the database tables.
    """
    print("Setting up the database...")
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create the 'Trade' table
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
    print("Table 'Trade' created.")

    # Create the 'TradeDay' table
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
    print("Table 'TradeDay' created.")

    # Create the 'Account' table
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
    print("Table 'Account' created.")

    # Create the 'api_keys' table
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY,
                api_key TEXT,
                api_secret TEXT
            )
        ''')
    print("Table 'api_keys' created.")

    conn.commit()
    conn.close()
    print("Database setup completed.")

def insert_dummy_data():
    """
    Insert dummy data into the database for testing and initial setup.
    """
    print("Inserting dummy data...")
    conn = get_db_connection()
    cursor = conn.cursor()

    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")

        # Insert 4 trades per day into 'Trade' table
        for j in range(4):
            cursor.execute('''
                        INSERT INTO Trade (symbol, side, entry_price, leverage, time_open, state, max_risk, trigger_safe_stop_loss, amount_safe_stop_loss, percentage, pnl)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', ('AAPL', 'Long', 150 + j, 2, date_str, 'Open', 0.1, 0.05, 0.1, 0.2, 50))

            # Insert a summary into 'TradeDay' table
        cursor.execute('''
                    INSERT INTO TradeDay (date, total_trades, avg_pnl, total_pnl, other_variables)
                    VALUES (?, ?, ?, ?, ?)
                ''', (date_str, 4, 0.05, 0.2, 'variable'))

        # Insert data into 'Account' table
        cursor.execute('''
                    INSERT INTO Account (datetime, account_balance, real_account_balance, margin_ratio, other_variables)
                    VALUES (?, ?, ?, ?, ?)
                ''', (date_str, 10000, 9500, 0.25, 'variable'))

    conn.commit()
    conn.close()
    print("Dummy data insertion completed.")

# Execute the setup and data insertion
setup_database()
insert_dummy_data()
