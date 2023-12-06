import sqlite3

from colorama import Fore

from api_calls.price import get_futures_current_price
from api_calls.trades import get_futures_positions_information
from bot import Bot
from config import db_path
from sqliteDB.db_actions import close_bot


# Function that gets open bots from database and creates instances of the Bot class
def get_open_bots_from_db(db_path):
    """
    Retrieves all open bots from the database.

    Parameters:
    db_path (str): Path to the database file.

    Returns:
    list: A list of tuples representing open bots.
    """

    open_bots = []

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, symbol, side FROM bot_status WHERE status='open'")
            open_bots = cursor.fetchall()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    return open_bots
