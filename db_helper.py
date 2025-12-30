import mysql.connector
from contextlib import contextmanager

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

@contextmanager
def get_db_cursor(commit=False):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        yield cursor
        if commit:
            connection.commit()
    finally:
        cursor.close()
        connection.close()

def fetch_expenses_for_date(expense_date):
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT amount, category, notes FROM expenses WHERE expense_date = %s",
            (expense_date,)
        )
        return cursor.fetchall()

def delete_expenses_for_date(expense_date):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "DELETE FROM expenses WHERE expense_date = %s",
            (expense_date,)
        )

def insert_expense(expense_date, amount, category, notes):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )