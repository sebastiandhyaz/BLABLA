from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from app.controllers import auth, patients

app.register_blueprint(auth.bp)
app.register_blueprint(patients.bp)

db.create_all()

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
