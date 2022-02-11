from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)

app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get("DATABASE_URL")

db=SQLAlchemy(app)

class Users(db.Model):
    """Create a table Users on the candidature database

    Args:
        db.Model: Generates columns for the table
        UserMixin: Generates an easy way to provide a current_user

    """
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    last_name = db.Column(db.String(length=30), nullable=False)
    first_name = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50),
                              nullable=False, unique=True)
    password_hash = db.Column(db.String(length=200), nullable=False)
    telephone_number = db.Column(db.String(length=10), nullable=True)
    promo = db.Column(db.String(length=30), nullable=True)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self):
        return f'{self.last_name} {self.first_name}'

    def json(self):
        return {
            'last_name': self.last_name,
            'first_name': self.first_name,
            'email_address': self.email_address,
            'telephone_number': self.telephone_number,
            'promo' : self.promo,
            'is_admin': self.is_admin
        }

    @classmethod
    def find_by_title(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def get_all_learner(cls):
        return cls.query.filter_by(is_admin = False).with_entities(Users.id, Users.promo).all()
    
    @classmethod
    def find_by_promo(cls, promo):
        return cls.query.filter_by(promo = promo).with_entities(Users.id, Users.promo).all()
    

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
   

