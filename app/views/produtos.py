from flask import Blueprint, render_template, request, redirect, url_for
from app.services.categorias import consultar_categorias
from app.services.produtos import consultar_estoque, produto_existe, cadastrar_produto, apagar_estoque, subtrair_produto, consultar_produto, somar_produto, descadastrar_produto
from datetime import date
bp = Blueprint("produtos", __name__)

@bp.route("/produtos/scan")
def scan():
    return render_template("produtos/scan.html")

@bp.route("/produtos/scan/verificar", methods=["POST"])
def verificar():
    codigo = request.form.get("codigo")
    if not codigo:
        return render_template("produtos/scan.html", erro="O codigo é obrigatorio!")
    produto = produto_existe(codigo)
    
    if produto:
        return redirect(url_for('produtos.gerenciar_produto', codigo=codigo))
    else:
        return redirect(url_for('produtos.cadastro', codigo=codigo))
    
@bp.route("/produtos/gerenciar_produto")
def gerenciar_produto():
    codigo = request.args.get("codigo")
    return render_template("produtos/gerenciar_produto.html", codigo=codigo)

@bp.route("/produtos/cadastro")
def cadastro():
    categorias = consultar_categorias()
    codigo = request.args.get("codigo")
    return render_template("produtos/cadastro.html", categorias=categorias, codigo=codigo)

@bp.route("/produto/infos", methods=["POST"])
def infos():
    codigo = request.form.get("codigo")
    nome = request.form.get("nome")
    categoria = request.form.get("categoria")
    quantidade = request.form.get("quantidade")
    categorias = consultar_categorias()
    data = date.today()
    if not codigo:
        return render_template("produtos/cadastro.html",
            erro = "O codigo é obrigatorio!",
            codigo=codigo,
            nome=nome,
            categoria=categoria,
            quantidade=quantidade,
            categorias=categorias
            )
    if not nome:
        return render_template("produtos/cadastro.html",
            erro = "O nome é obrigatorio!",
            codigo=codigo,
            nome=nome,
            categoria=categoria,
            quantidade=quantidade,
            categorias=categorias
            )
    if not categoria:
        return render_template("produtos/cadastro.html",
            erro = "O categoria é obrigatorio!",
            codigo=codigo,
            nome=nome,
            categoria=categoria,
            quantidade=quantidade,
            categorias=categorias
            )
    if not quantidade:
        return render_template("produtos/cadastro.html",
            erro = "O quantidade é obrigatorio!",
            codigo=codigo,
            nome=nome,
            categoria=categoria,
            quantidade=quantidade,
            categorias=categorias
            )
    if categoria == "nova_categoria":
        return redirect(url_for('categorias.cadastro'))
    cadastrar_produto(codigo, nome, categoria, quantidade, data)
    return redirect(url_for('produtos.estoque'))

@bp.route("/produtos/deletar/confirmar")
def confirmar():
    return render_template("produtos/confirmaçao_produtos.html")

@bp.route("/produtos/deletar")
def deletar():
    apagar_estoque()
    return redirect(url_for("produtos.estoque"))

@bp.route("/produtos/subtrair/num", methods=["POST","GET"])
def subtrair_num():
    codigo = request.form.get("codigo")
    return render_template("produtos/subtrair_num.html", codigo = codigo)
    
@bp.route("/produtos/somar/num", methods=["POST","GET"])
def somar_num():
    codigo = request.form.get("codigo")
    return render_template("produtos/somar_num.html", codigo = codigo)

@bp.route("/produtos/subtrair", methods=["POST","GET"])
def subtrair():
    codigo = request.form.get("codigo")
    num = request.form.get("subtrair_num")
    subtrair_produto(codigo,num)
    return redirect(url_for("produtos.produto", codigo=codigo))

@bp.route("/produtos/somar", methods=["POST","GET"])
def somar():
    codigo = request.form.get("codigo")
    num = request.form.get("somar_num")
    somar_produto(codigo,num)
    return redirect(url_for("produtos.produto", codigo=codigo))

@bp.route("/produtos/confirmação_descadastro")
def confirmação_descadastro():
    codigo = request.args.get("codigo")
    return render_template("produtos/confirmação_descadastro.html", codigo=codigo)

@bp.route("/produtos/descadastrar")
def descadastrar():
    codigo = request.args.get("codigo")
    descadastrar_produto(codigo)
    return redirect(url_for("produtos.estoque"))
    

@bp.route("/produtos/produto", methods=["POST","GET"])
def produto():
    if request.method == "POST":
        codigo = request.form.get("codigo")
    else:
        codigo = request.args.get("codigo")
    relatorio = consultar_produto(codigo)
    return render_template("produtos/produto.html", relatorio=relatorio)

@bp.route("/produtos/estoque")
def estoque():
    estoque = consultar_estoque()
    return render_template("produtos/estoque.html", estoque=estoque)