from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
# Initialize Flask App
app = Flask(__name__)

# Database file
DATABASE_FILE = "trading_journal.db"

# Database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# Route for homepage
@app.route('/')
def index():
    conn = get_db_connection()
    trades = conn.execute('SELECT * FROM Trade').fetchall()
    trade_days = conn.execute('SELECT * FROM TradeDay').fetchall()
    account_data = conn.execute('SELECT * FROM Account').fetchall()
    conn.close()

    return render_template('index.html', trades=trades, trade_days=trade_days, account_data=account_data)

@app.route('/dashboard')
def dashboard():

    # Fetch data for the Dashboard
    return render_template('dashboard.html')

@app.route('/objectives')
def objectives():
    # Fetch data for the Objectives
    return render_template('objectives.html')

@app.route('/trading-diary')
def trading_diary():
    # Fetch data for the Trading Diary
    return render_template('trading_diary.html')

@app.route('/options')
def options():
    # Data for options, if any
    return render_template('options.html')

@app.route('/api-management', methods=['GET', 'POST'])
def api_management():
    if request.method == 'POST':
        api_key = request.form['apiKey']
        api_secret = request.form['apiSecret']

        conn = get_db_connection()
        conn.execute('INSERT INTO api_keys (api_key, api_secret) VALUES (?, ?)',
                     (api_key, api_secret))
        conn.commit()
        conn.close()
        return redirect(url_for('api_management'))

    conn = get_db_connection()
    api_keys = conn.execute('SELECT * FROM api_keys').fetchall()
    conn.close()
    return render_template('api_management.html', api_keys=api_keys)


# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
