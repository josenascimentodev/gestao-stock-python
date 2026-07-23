from app.database import get_db

def cadastrar_produto(codigo, nome, categoria, quantidade, data):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO PRODUTOS (CODIGO, NOME, CATEGORIA, QUANTIDADE, DATA) VALUES (?, ?, ?, ?, ?)", (codigo, nome, categoria, quantidade, data))
    db.commit()

def descadastrar_produto(codigo):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM PRODUTOS WHERE CODIGO = ?", (codigo,))
    db.commit()

def consultar_produto(codigo):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM PRODUTOS WHERE CODIGO = ?", (codigo,))
    return cursor.fetchone()

def consultar_estoque():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM PRODUTOS")
    return cursor.fetchall()

def apagar_estoque():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM PRODUTOS")
    db.commit()

def produto_existe(codigo):
    return consultar_produto(codigo)

def somar_produto(codigo, quantidade):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE PRODUTOS SET QUANTIDADE = QUANTIDADE + ? WHERE CODIGO = ?", (quantidade, codigo))
    db.commit()

def subtrair_produto(codigo, quantidade):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE PRODUTOS SET QUANTIDADE = QUANTIDADE - ? WHERE CODIGO = ?", (quantidade, codigo))
    db.commit()