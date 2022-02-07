from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .notifs import math_relance

app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from App import routes
from App import models

app.jinja_env.globals.update(math_relance=math_relance)

#models.init_db()
