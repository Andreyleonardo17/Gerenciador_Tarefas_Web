from app.extensions import db, bcrypt, user_mixin

class User(user_mixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    tasks = db.relationship('Task', backref='autor', lazy=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = self.hash_password(password)

    def hash_password(self, new_password):
        return bcrypt.generate_password_hash(new_password).decode('utf-8')


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))
    status = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, title, description, user_id):
        self.title = title
        self.description = description
        self.user_id = user_id