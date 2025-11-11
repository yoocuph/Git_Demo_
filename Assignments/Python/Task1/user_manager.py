import sqlite3

DB_NAME = "mindfuel.db"

def add_user(name, email, status="active", frequency="daily"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, status, frequency) VALUES (?, ?, ?, ?)",
            (name, email, status, frequency)
        )
        conn.commit()
        print(f"Added user: {name} ({email})")
    except sqlite3.IntegrityError:
        print("Error: That email is already subscribed.")
    finally:
        conn.close()


def list_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, status, frequency FROM users")
    users = cursor.fetchall()
    conn.close()

    print("\n Subscribers List:")
    for u in users:
        print(u)


def update_status(email, new_status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET status = ? WHERE email = ?", (new_status, email))
    conn.commit()
    conn.close()
    print(f"Updated {email} to '{new_status}'")


def delete_user(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE email = ?", (email,))
    conn.commit()
    conn.close()
    print(f"Deleted user with email: {email}")


if __name__ == "__main__":
    users = [
        ("Yussuf Alade", "yoocuph@gmail.com", "active", "daily"),
        ("Kabir Mohammed", "kabirolawalemohammed@gmail.com", "active", "daily"),
        ("AbdulRahMan Ibrahim", "abdrahman24434@gmail.com", "active", "daily"),
        ("Olukayode Olusegun", "olukayodeoluseguno@gmail.com", "active", "daily"),
        ("Ajiboye Feyisayo", "solapeajiboye@gmail.com", "active", "daily"),
        ("Khabirat Ajibade", "khabiratajibade20@gmail.com", "active", "daily"),
    ]

    for name, email, status, freq in users:
        add_user(name, email, status, freq)

    list_users()

