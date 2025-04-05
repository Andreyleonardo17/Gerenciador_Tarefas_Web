from flask import Flask
import os
from dotenv import load_dotenv
from app.auth import auth_bp
from app.extensions import db, migrate, bcrypt

def create_app():

    # Instanciando a classe Flask
    app = Flask(__name__)

    load_dotenv()

    # Configurando o banco de dados SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dados.db"
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    # Inicializando o app (instancia Flask) com a extensão
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    app.register_blueprint(auth_bp)

    with app.app_context():
        from . import models
        db.create_all()

    return app