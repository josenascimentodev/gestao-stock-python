from flask import Flask
from app.views.home import bp as home_bp
from app.views.produtos import bp as produtos_bp
from app.views.categorias import bp as categorias_bp
from app.database import close_db, init_db

def create_app():
    app = Flask(__name__)

    app.register_blueprint(home_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(categorias_bp)

    app.teardown_appcontext(close_db)

    with app.app_context():
        init_db()

    return app