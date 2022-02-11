from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)

app.config.from_object('config')
app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get("DATABASE_URL")
db=SQLAlchemy(app)
db.init_app()
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'simplon.bot@gmail.com',
    "MAIL_PASSWORD": 'simplon@59'
}

app.config.update(mail_settings)
mail = Mail(app)


from App import routes
from App import models



#models.init_db()