import mysql.connector
from contextlib import contextmanager
from logger_config import setup_logger

# ✅ Logger added
logger = setup_logger("db_helper")

def get_db_connection():
    logger.info("Creating database connection")
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
    )

@contextmanager
def get_db_cursor(commit=False):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        yield cursor
        if commit:
            connection.commit()
            logger.info("Database changes committed")
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise
    finally:
        cursor.close()
        connection.close()
        logger.info("Database connection closed")

def fetch_expenses_for_date(expense_date):
    logger.info(f"Fetching expenses for date: {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT amount, category, notes FROM expenses WHERE expense_date = %s",
            (expense_date,)
        )
        return cursor.fetchall()

def delete_expenses_for_date(expense_date):
    logger.info(f"Deleting expenses for date: {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "DELETE FROM expenses WHERE expense_date = %s",
            (expense_date,)
        )

def insert_expense(expense_date, amount, category, notes):
    logger.info(
        f"Inserting expense | Date: {expense_date}, Amount: {amount}, Category: {category}"
    )
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )