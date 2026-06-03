import sqlite3

def create_user_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


def register(username,password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users VALUES (?,?)",
            (username,password)
        )
        conn.commit()
        return True
    except:
        return False


def login(username,password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username,password)
    )

    user = c.fetchone()
    conn.close()

    return user is not None