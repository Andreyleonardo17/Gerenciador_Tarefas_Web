from flask import render_template, request, Blueprint, redirect, url_for
from app.models import User
from flask_login import login_user, login_required, logout_user
from app.extensions import db, login_manager, bcrypt

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def user_loader(id):
    return db.session.query(User).filter_by(id=id).first()

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

            login_user(new_user)

            return redirect(url_for('routes.home'))
        else:
            return "Senhas diferentes"

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['emailForm']
        senha = str(request.form['senhaForm'])

        user = db.session.query(User).filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, senha):
            login_user(user)
            return redirect(url_for('routes.task'))


@auth_bp.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return render_template('logout.html')


