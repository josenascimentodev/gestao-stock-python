import sqlite3
from flask import g

DATABASE = "instance/estoque.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row

    return g.db

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS CATEGORIAS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NOME TEXT NOT NULL UNIQUE
                    )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PRODUTOS (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    CODIGO TEXT NOT NULL UNIQUE,
                    NOME TEXT NOT NULL,
                    QUANTIDADE INTEGER NOT NULL,
                    CATEGORIA TEXT NOT NULL,
                    DATA TEXT NOT NULL
                    )
        """)


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()