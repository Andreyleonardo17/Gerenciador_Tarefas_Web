from os import abort
from flask import Blueprint, render_template, request, redirect, url_for
from app.models import User, Task
from flask_login import login_required, current_user
from app.extensions import db

routes_bp = Blueprint('routes', __name__)

@routes_bp.route("/", methods=["GET"])
def home():
    return render_template('home.html')

@routes_bp.route("/tasks", methods=["GET", "POST"])
@login_required
def task():
    if request.method == 'GET':
        my_tasks_pending = db.session.query(Task).filter_by(user_id=current_user.id, status=False).all()
        my_tasks_completed = db.session.query(Task).filter_by(user_id=current_user.id, status=True).all()
    return render_template('tasks.html', tarefas_pendentes=my_tasks_pending, tarefas_concluidas=my_tasks_completed, nome= current_user.name)

@routes_bp.route("/add_task", methods=["GET", "POST"])
@login_required
def add_task():
    if request.method == 'GET':
        return render_template('add_task.html')
    elif request.method == 'POST':
        titulo = request.form['titleForm']
        descricao = request.form['descriptionForm']

        new_task = Task(title=titulo, description=descricao, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('routes.task'))

@routes_bp.route("/edit_task/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_task(id):
    if request.method == 'GET':
        task_to_edit = db.session.query(Task).filter_by(id=id).first()

        return render_template('edit_task.html', tarefa=task_to_edit)
    elif request.method == 'POST':
        titulo = request.form['titleForm']
        descricao = request.form['descriptionForm']

        task_to_edit = db.session.query(Task).filter_by(id=id).first()
        task_to_edit.title = titulo
        task_to_edit.description = descricao
        db.session.commit()

        return redirect(url_for('routes.task'))

@routes_bp.route("/completed/<int:id>", methods=['POST'])
@login_required
def complet_task(id):
    if request.method == 'POST':
        task_to_complet = db.session.query(Task).filter_by(id=id).first()
        task_to_complet.status = True
        db.session.commit()

        return redirect(url_for('routes.task'))

@routes_bp.route("/delete_task/<int:id>/confirm")
@login_required
def confirm_delete(id):
    task_to_delete = db.session.query(Task).filter_by(id=id).first()

    if not task_to_delete:
        abort(403)

    if task_to_delete.user_id != current_user.id:
        abort(403)

    return render_template('confirm_delete.html', tarefa=task_to_delete)

@routes_bp.route("/delete/<int:id>", methods=['POST'])
@login_required
def delete_task(id):
    task_to_delete = db.session.query(Task).filter_by(id=id).first()

    if not task_to_delete:
        abort(403)

    if task_to_delete.user_id != current_user.id:
        abort(403)

    db.session.delete(task_to_delete)
    db.session.commit()

    return redirect(url_for('routes.task'))
