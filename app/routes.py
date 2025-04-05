from flask import Blueprint, render_template

routes_bp = Blueprint('routes', __name__)

@routes_bp.route("/", methods=["GET"])
def home():
    return render_template('home.html')