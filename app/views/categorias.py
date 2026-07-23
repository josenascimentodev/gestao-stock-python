from flask import Blueprint, render_template, request, redirect, url_for
from app.services.categorias import consultar_categorias, cadastrar, apagar_categorias, descadastrar_categoria

bp = Blueprint("categorias", __name__)

@bp.route("/categorias/gerenciar")
def gerenciar_categorias():
    return render_template("categorias/gerenciar_categorias.html")

@bp.route("/categorias/cadastro")
def cadastro():
    return render_template("categorias/categoria_cadastro.html")

@bp.route("/categorias/descadastrar/info")
def descadastrar_info():
    categorias = consultar_categorias()
    return render_template("categorias/descadastrar_info.html",categorias=categorias) 

@bp.route("/categorias/descadastrar", methods=["POST"])
def descadastrar():
    categoria = request.form.get("categoria")
    descadastrar_categoria(categoria)
    return redirect(url_for("categorias.categorias"))
    
    
@bp.route("/categorias/infos", methods=["POST"])
def infos():
    categoria = request.form.get("categoria")
    cadastrar(categoria)
    return redirect(url_for("categorias.categorias"))

@bp.route("/categorias/confirmar")
def confirmar():
    return render_template("categorias/confirmaçao.html")

@bp.route("/categorias/deletar")
def deletar():
    apagar_categorias()
    return redirect(url_for('categorias.categorias'))
    

@bp.route("/categorias/categorias", methods=["GET", "POST"])
def categorias():
    categorias = consultar_categorias()
    return render_template("categorias/categorias.html", categorias=categorias)