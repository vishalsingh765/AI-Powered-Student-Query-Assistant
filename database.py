import sqlite3

def create_tables():
    conn = sqlite3.connect("chat_logs.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS chats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        question TEXT,
        response TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_chat(user, question, response):
    conn = sqlite3.connect("chat_logs.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO chats(user,question,response) VALUES(?,?,?)",
        (user, question, response)
    )

    conn.commit()
    conn.close()