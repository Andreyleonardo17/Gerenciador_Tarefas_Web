from flask import Blueprint, jsonify, request, abort
from app.extensions import db, bcrypt
from app.models import Task, User
from flask_login import login_user, login_required, logout_user, current_user

api_bp = Blueprint('api', __name__)

def to_dict(task_object):
    return {
        "id": task_object.id,
        "title": task_object.title,
        "description": task_object.description,
        "status": task_object.status,
        "user_id": task_object.user_id
    }

def get_task_or_abort(id):
    task = db.session.query(Task).filter_by(id=id).first()
    if not task:
        abort(404, descripition="Task não encontrada")
    if task.user_id != current_user.id:
        abort(404, descripition="Acesso negado")
    return task

@api_bp.route("/api/login", methods=['POST'])
def api_login():
    user = request.json
    if all(key in user for key in ("email", "password")):
        user_db = db.session.query(User).filter_by(email=user["email"]).first()
        if user_db and bcrypt.check_password_hash(user_db.password, user["password"]):
            login_user(user_db)
            return jsonify({"success": f"Usuário {user_db.id} Logado"}), 200

    return jsonify({"error": "Requisicao incorreta"}), 400

@api_bp.route("/api/tasks", methods= ['GET'])
@login_required
def api_tasks():
    tasks = db.session.query(Task).filter_by(user_id=current_user.id).all()
    return jsonify([to_dict(task) for task in tasks]), 200

@api_bp.route("/api/add_task", methods= ['POST'])
@login_required
def api_add_task():
    new_task = request.json
    if all(key in new_task for key in ("description", "title")):
        task = Task(title=new_task["title"], description=new_task["description"], user_id=current_user.id)
        db.session.add(task)
        db.session.commit()

        return jsonify(to_dict(task)), 201
    return jsonify({"error": "Requisicao incorreta"}), 400

@api_bp.route("/api/edit_task/<int:id>", methods= ['PUT'])
@login_required
def api_edit_task(id):
    new_task = request.json
    if all(key in new_task for key in ("description", "title", "status")):
        task_to_edit = get_task_or_abort(id)
        task_to_edit.title = new_task["title"]
        task_to_edit.description = new_task["description"]
        task_to_edit.status = new_task["status"]
        db.session.commit()

        return jsonify(to_dict(task_to_edit)), 200
    return jsonify({"error": "Requisicao incorreta"}), 400

@api_bp.route("/api/delete_task/<int:id>", methods= ['DELETE'])
@login_required
def api_delete_task(id):
    task_to_delete = get_task_or_abort(id)
    db.session.delete(task_to_delete)
    db.session.commit()

    return jsonify({"success": "Tarefa deletada"}), 200