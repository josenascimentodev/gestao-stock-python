import sqlite3
import datetime

base = sqlite3.connect("estoque.db")
cursor = base.cursor()

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

def pedir_codigo():
    while True:
        codigo = input("\nDigite o código do produto: ")
        if codigo:
            return codigo
        else:
            print("Código do produto não pode ser vazio. Tente novamente.")

def pedir_nome():
    while True:
        nome = input("\nDigite o nome do produto: ")
        if nome:
            return nome
        else:
            print("Nome do produto não pode ser vazio. Tente novamente.")

def pedir_quantidade():
    while True:
        try:
            quantidade = int(input("\nDigite a quantidade do produto: "))
            if quantidade >= 0:
                return quantidade
            else:
                print("Quantidade deve ser um número inteiro positivo. Tente novamente.")
        except ValueError:
            print("Quantidade deve ser um número inteiro. Tente novamente.")

def pedir_categoria_existente():
    while True:
        print("\nCategorias disponíveis:")
        for categoria in consultar_categorias():
            print(categoria[1])
        categoria = input("\nDigite a categoria: ")
        if categoria in [cat[1] for cat in consultar_categorias()]:
            return categoria
        else:
            print("Categoria não encontrada. Tente novamente.")

def criar_categoria():
    while True:
        categoria = input("\nDigite a nova categoria: ")
        if categoria not in [cat[1] for cat in consultar_categorias()]:
            cursor.execute("INSERT INTO CATEGORIAS (NOME) VALUES (?)", (categoria,))
            base.commit()
            return categoria
        else:
            print("Categoria já cadastrada. Tente novamente.")

def cadastrar_produto(codigo, nome, categoria, quantidade, data):
    cursor.execute("INSERT INTO PRODUTOS (CODIGO, NOME, CATEGORIA, QUANTIDADE, DATA) VALUES (?, ?, ?, ?, ?)", (codigo, nome, categoria, quantidade, data))
    base.commit()

def descadastrar_produto(codigo):
    cursor.execute("DELETE FROM PRODUTOS WHERE CODIGO = ?", (codigo,))
    base.commit()

def descadastrar_categoria(categoria):
    cursor.execute("DELETE FROM CATEGORIAS WHERE NOME = ?", (categoria,))
    base.commit()

def consultar_categorias():
    cursor.execute("SELECT * FROM CATEGORIAS")
    return cursor.fetchall()

def apagar_categorias():
    cursor.execute("DELETE FROM CATEGORIAS")
    base.commit()

def adicionar_produto(codigo, quantidade):
    cursor.execute("UPDATE PRODUTOS SET QUANTIDADE = QUANTIDADE + ? WHERE CODIGO = ?", (quantidade, codigo))
    base.commit()

def remover_produto(codigo, quantidade):
    cursor.execute("UPDATE PRODUTOS SET QUANTIDADE = QUANTIDADE - ? WHERE CODIGO = ?", (quantidade, codigo))
    base.commit()

def consultar_produto(codigo):
    cursor.execute("SELECT * FROM PRODUTOS WHERE CODIGO = ?", (codigo,))
    return cursor.fetchone()

def consultar_estoque():
    cursor.execute("SELECT * FROM PRODUTOS")
    return cursor.fetchall()

def apagar_estoque():
    cursor.execute("DELETE FROM PRODUTOS")
    base.commit()

def mostrar_menu(n_menu):
    if n_menu == 1:
        while True:
            print("-" * 40)
            print("Menu principal:")
            print("1 - Escanear produto")
            print("2 - Gerenciar categorias")
            print("3 - consultar estoque")
            print("0 - Sair")
            try:
                resposta = int(input("\nEscolha uma opção: "))
                if resposta in [0, 1, 2, 3, 1010, 1011]:
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Opção inválida. Tente novamente.")
    elif n_menu == 2:
        while True:
            print("1 - Cadastrar categoria")
            print("2 - Descadastrar categoria")
            print("3 - Consultar categorias")
            try:
                resposta = int(input("\nEscolha uma opção: "))
                if resposta in [1, 2, 3]:
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Opção inválida. Tente novamente.")
    elif n_menu == 3:
        while True:
            print("1 - Adicionar produto")
            print("2 - Remover produto")
            print("3 - Consultar produto")
            print("4 - Descadastrar produto")
            try:
                resposta = int(input("\nEscolha uma opção: "))
                if resposta in [1, 2, 3, 4]:
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Opção inválida. Tente novamente.")
    elif n_menu == 4:
        while True:
            print("1 - Cadastar produto")
            print("2 - Cadastar produto e categoria")
            try:
                resposta = int(input("\nEscolha uma opção: "))
                if resposta in [1,2]:
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Opção inválida. Tente novamente.")
    return resposta

def main():
    while True:
        resposta = mostrar_menu(1)
        if resposta == 1:
            print("Escanear produto...")
            codigo = pedir_codigo()
            produto = consultar_produto(codigo)
            if produto:
                print("\nProduto encontrado!")
                resposta = mostrar_menu(3)
                if resposta == 1:
                    print("Adicionar produto...")
                    quantidade = pedir_quantidade()
                    adicionar_produto(codigo, quantidade)
                    print("Produto adicionado!")
                elif resposta == 2:
                    print("Remover produto...")
                    while True:
                        quantidade = pedir_quantidade()
                        if quantidade > produto[3]:
                            print("\nQuantidade a ser removida é maior do que a quantidade em estoque. Tente novamente.")
                        else:
                            break
                    remover_produto(codigo, quantidade)
                    print("Produto removido!")
                elif resposta == 3:
                    print("consultar produto...")
                    print("-" * 40)
                    print(f"Código: {produto[1]}\nProduto: {produto[2]}\nQuantidade: {produto[3]}\nCategoria: {produto[4]}\nData de cadastro: {produto[5]}")
                elif resposta == 4:
                    print("Descadastrar produto...")
                    print("Produto descadastrado")
                    descadastrar_produto(codigo)
            else:
                print("\nProduto não encontrado!")
                resposta = mostrar_menu(4)
                if resposta == 1:
                    print("Cadastrar produto...\n")
                    nome = pedir_nome()
                    if consultar_categorias():
                        categoria = pedir_categoria_existente()
                    else:
                        categoria = criar_categoria()
                    quantidade = pedir_quantidade()
                    data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cadastrar_produto(codigo, nome, categoria, quantidade, data)
                elif resposta == 2:
                    print("Criar e cadastrar produto...")
                    nome = pedir_nome()
                    categoria = criar_categoria()
                    quantidade = pedir_quantidade()
                    data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cadastrar_produto(codigo, nome, categoria, quantidade, data)
                    print("Produto e categoria cadastrado!")
        elif resposta == 2:
            print("Gerenciar categorias...\n")
            resposta = mostrar_menu(2)
            if resposta == 1:
                print("Cadastrar categoria...")
                categoria = criar_categoria()
                print("Categoria cadastrada!")
            elif resposta == 2:
                print("Descadastrar categoria...")
                if consultar_categorias():
                    categoria = pedir_categoria_existente()
                    descadastrar_categoria(categoria)
                    print(f"Categoria {categoria} foi removida")
                else:
                    print("\nNão há categorias disponiveis")
            elif resposta == 3:
                print("Consultar categoria...")
                if consultar_categorias():
                    print("\nCategorias cadastradas:")
                    for categoria in consultar_categorias():
                        print(categoria[1])
                else:
                    print("\nNão há categorias disponiveis")
        elif resposta == 3:
            print("consultar estoque...")
            if consultar_estoque():
                for produto in consultar_estoque():
                    print("-" * 40)
                    print(f"Código: {produto[1]}\nProduto: {produto[2]}\nQuantidade: {produto[3]}\nCategoria: {produto[4]}\nData de cadastro: {produto[5]}")
            else:
                print("Não há produtos disponiveis")
        elif resposta == 1010:
            apagar_estoque()
            print("Limpar estoque...")
            print("\nEstoque apagado com sucesso!")
        elif resposta == 1011:
            apagar_categorias()
            print("Limpar categorias...")
            print("\nCategorias apagadas com sucesso!")
        elif resposta == 0:
            print("Saindo...")
            break

try:
    main()

finally:
    base.close()