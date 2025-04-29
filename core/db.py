import sqlite3
from flask import g

def init_db(app):
    with app.app_context():
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS POLL (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS CHOICES(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                poll_id INTEGER NOT NULL,
                choice_text TEXT NOT NULL,
                VOTES INTEGER DEFAULT 0,
                FOREIGN KEY (poll_id) REFERENCES POLL(id)                    
            )
        ''')
        conn.commit()
        conn.close()

import sqlite3
from flask import g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('your_database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def modify_db(query, args=()):
    db = get_db()
    db.execute(query, args)
    db.commit()
