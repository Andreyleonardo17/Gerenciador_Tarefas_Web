from flask import render_template, request, Blueprint
from app.models import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        email = request.form['emailForm']
        senha = request.form['senhaForm']
        confirmacao = request.form['confirmacaoForm']

        if senha == confirmacao:
            new_user = User(name=nome, email=email, password=senha)
            db.session.add(new_user)
            db.session.commit()
            return "Usuário cadastrado"
        else:
            return "Senhas diferentes"