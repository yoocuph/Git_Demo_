import sqlite3

def create_users_table():
    # Connect to (or create) a database file
    conn = sqlite3.connect("mindfuel.db")
    cursor = conn.cursor()

    # Create a users table if it doesn't already exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            status TEXT CHECK(status IN ('active', 'inactive')) DEFAULT 'active',
            frequency TEXT CHECK(frequency IN ('daily', 'weekly')) DEFAULT 'daily'
        )
    """)

    conn.commit()
    conn.close()
    print("Users table created successfully!")

if __name__ == "__main__":
    create_users_table()
