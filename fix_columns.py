
import sqlite3
import os

def fix_columns():
    db_file = 'test_wise.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Rename q_TEXT back to q_date in quiz_det
    try:
        # Check if q_TEXT exists
        cursor.execute("SELECT q_TEXT FROM quiz_det LIMIT 1")
        print("Renaming q_TEXT to q_date in quiz_det...")
        # SQLite 3.25+ supports RENAME COLUMN
        cursor.execute("ALTER TABLE quiz_det RENAME COLUMN q_TEXT TO q_date")
    except sqlite3.OperationalError:
        print("q_TEXT not found or already renamed.")

    conn.commit()
    conn.close()
    print("Database columns fixed.")

if __name__ == '__main__':
    fix_columns()
