from app import db, bcrypt
from app import login_manager
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    @classmethod
    def create_user(cls, name, username, email, password):
        user = cls(
            name = name,
            email = email,
            username = username,
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        )

        return user

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    edit_date = db.Column(db.DateTime, nullable=True)

    @classmethod
    def create_post(cls, title, content, user_id, category_id=None):
        post = cls(
            title = title,
            content = content,
            user_id = user_id,
            category_id = category_id
        )

        return post