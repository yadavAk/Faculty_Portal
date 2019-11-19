from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from facultyportal.config import Config
from facultyportal import mongo_setup

# export FLASK_APP=facultyportal.py
# export FLASK_DEBUG=1
# flask run

db = SQLAlchemy()
mongo_setup.global_init()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from facultyportal.users.routes import users
    from facultyportal.posts.routes import posts
    from facultyportal.main.routes import main
    from facultyportal.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

