from flask import Flask
from dotenv import load_dotenv
from app.extensions import db, migrate, bcrypt, login_manager
import os

from app.routes import routes_bp
from app.auth import auth_bp

def create_app():

    # Instanciando a classe Flask
    app = Flask(__name__)
    app.secret_key = 'chave_teste'

    # Carrega as variáveis do ambiente
    load_dotenv()

    # Configurando o banco de dados SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dados.db"
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    # Inicializa o SQLAlchemy com a instância do app Flask. Isso conecta o ORM com o app.
    db.init_app(app)

    # nicializa o Flask-Migrate, permitindo criar e gerenciar versões do banco de dados com comandos como flask db migrate.
    migrate.init_app(app, db)

    # Inicializa o bcrypt para poder hashear senhas de forma segura dentro do app.
    bcrypt.init_app(app)

    # Inicializando o LoginManager para porder controlar o acesso de usuários logaods
    login_manager.init_app(app)

    # Registra o blueprint de autenticação com o app principal. Assim, as rotas definidas em auth.py ficam disponíveis.
    app.register_blueprint(auth_bp)

    app.register_blueprint(routes_bp)

    with app.app_context():
        from . import models
        db.create_all()

    return app