import sqlite3


def connect_db(db_path):
    """ Create a database connection. """
    return sqlite3.connect(db_path)


def execute_db_query(db_path, query, params=()):
    """ Execute a database query """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid

def close_bot(db_path, botName):
    """ Marks the bot's status as closed in the database. """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE bot_status SET
            status = "closed"
            WHERE bot_name = ? AND status = "open"
        ''', (botName,))
        conn.commit()
        return cursor.lastrowid


# TODO: Solve zhe 10%