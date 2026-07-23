from app.database import get_db

def cadastrar(categoria):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO CATEGORIAS (NOME) VALUES (?)", (categoria,))
    db.commit()
    return categoria

def descadastrar_categoria(categoria):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM CATEGORIAS WHERE NOME = ?", (categoria,))
    db.commit()

def consultar_categorias():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM CATEGORIAS")
    return cursor.fetchall()

def apagar_categorias():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM CATEGORIAS")
    db.commit()