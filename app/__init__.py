from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

db = SQLAlchemy()

def create_app():
    # Instanciando a classe Flask
    app = Flask(__name__)

    load_dotenv()

    # Configurando o banco de dados SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dados.db"
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    # Inicializando o app (instancia Flask) com a extensão
    db.init_app(app)

    with app.app_context():
        from . import models
        db.create_all()

    return app