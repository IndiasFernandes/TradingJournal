import sqlite3

def initialize_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()



    # Create a table for storing trade information
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trades (
        trade_id INTEGER PRIMARY KEY,
        symbol TEXT NOT NULL,
        side TEXT NOT NULL,
        price REAL NOT NULL,
        amount REAL NOT NULL,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    # Create a table for storing order information
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        symbol TEXT NOT NULL,
        order_type TEXT NOT NULL,
        side TEXT NOT NULL,
        price REAL,
        amount REAL NOT NULL,
        status TEXT NOT NULL,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    # Create a table for tracking open positions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS positions (
        position_id INTEGER PRIMARY KEY,
        symbol TEXT NOT NULL,
        side TEXT NOT NULL,
        entry_price REAL NOT NULL,
        amount REAL NOT NULL,
        time_opened TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        time_closed TIMESTAMP,
        close_price REAL
    );
    ''')

    # Create a table for tracking balance
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS balance (
        record_id INTEGER PRIMARY KEY,
        balance REAL NOT NULL,
        balance_in_trade REAL NOT NULL,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    # Create a table for storing configuration parameters
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS configuration (
        config_id INTEGER PRIMARY KEY,
        parameter TEXT NOT NULL,
        value TEXT NOT NULL,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    # Create a table for event logging
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS event_logs (
        log_id INTEGER PRIMARY KEY,
        level TEXT NOT NULL,
        message TEXT NOT NULL,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bot_status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bot_name TEXT NOT NULL,
        status TEXT NOT NULL, -- 'open' or 'closed'
        symbol TEXT,
        side TEXT,
        leverage REAL,
        actualPnL REAL,
        actualPercentage REAL,
        investedAmountInDollar REAL,
        investedAmountInCurrency REAL,
        entryPrice REAL,
        currentPrice REAL,
        stop_loss TEXT,
        take_profit TEXT,
        trailing_stop TEXT,
        stop_loss_plus TEXT,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')


    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_db('trading_bot.db')
