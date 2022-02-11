from App import db,login_manager
import datetime 
from flask_login import UserMixin # allow to set variable is_active=True and to stay connected
import logging as lg
from werkzeug.security import generate_password_hash
import csv
from flask import jsonify

@login_manager.user_loader
def load_user(user_id):
    """Allow to create a current_user with his id

    Args:
        user_id (int): user_id from the database

    Returns:
        instance of users depending of his id
    """
    return Users.query.get(int(user_id))

class Users(db.Model,UserMixin):
    """Create a table Users on the candidature database

    Args:
        db.Model: Generates columns for the table
        UserMixin: Generates an easy way to provide a current_user

    """
    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    last_name = db.Column(db.String(length=30), nullable=False)
    first_name = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=200), nullable=False)
    telephone_number = db.Column(db.String(length=10), nullable=True)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self):
        return f'{self.last_name} {self.first_name}'

    def json(self):
        return {
            'last_name': self.last_name, 
            'first_name': self.first_name,
            'email_address': self.email_address,
            'telephone_number': self.telephone_number,
            'is_admin': self.is_admin
            }

    @classmethod
    def find_by_title(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Candidacy(db.Model):
    """Create a table Candidacy on the candidature database

    Args:
        db.Model: Generates columns for the table

    """

    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'),nullable=False)
    plateforme = db.Column(db.String(), nullable=True)
    poste = db.Column(db.String(), nullable=True)
    entreprise = db.Column(db.String(), nullable=False)
    activite = db.Column(db.String(), nullable=True)
    type = db.Column(db.String(), nullable=True)
    lieu = db.Column(db.String(), nullable=True)
    contact_full_name = db.Column(db.String(length=50), nullable=False)
    contact_email = db.Column(db.String(length=50), nullable=True)
    contact_mobilephone = db.Column(db.String(length=50), nullable=True)
    date = db.Column(db.String(), default=datetime.date.today())
    status = db.Column(db.String(), nullable=True, default="En cours")
    relance = db.Column(db.Boolean,nullable=False, default=False)

    def __repr__(self):
        return f' Candidat id : {self.user_id}'

    def json(self):
        return {
            'id': self.id, 
            'user_id': self.user_id, 
            'plateforme': self.plateforme,
            'poste': self.poste,
            'entreprise': self.entreprise,
            'activite': self.activite,
            'type': self.type,
            'lieu': self.lieu,
            'contact_full_name': self.contact_full_name,
            'contact_email': self.contact_email,
            'contact_mobilephone': self.contact_mobilephone,
            'date': self.date,
            'status': self.status,
            'relance': self.relance
            }


    @classmethod
    def find_by_user_id(cls, user_id):
        candidacy_list=[]
        for candidacy in cls.query.filter_by(user_id=user_id).all():
            candidacy_list.append(candidacy.json())
        return candidacy_list

    @classmethod
    def get_all_in_list_with_user_name(cls):
        candidacy_list=[]
        for candidacy in cls.query.join(Users).with_entities(Users.first_name, cls.plateforme, cls.poste, cls.entreprise, cls.activite, cls.type, cls.lieu,  cls.contact_full_name, cls.contact_email, cls.contact_mobilephone,cls.date,cls.status).all():
            candidacy_list.append(candidacy)
        return candidacy_list

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        

class Offer(db.Model):
    """Create a table Offer on the candidature database

    Args:
        db.Model: Generates columns for the table

    """

    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'),nullable=False)
    lien = db.Column(db.String(), nullable=True)
    poste = db.Column(db.String(), nullable=True)
    entreprise = db.Column(db.String(), nullable=False)
    activite = db.Column(db.String(), nullable=True)
    type = db.Column(db.String(), nullable=True)
    lieu = db.Column(db.String(), nullable=True)
    contact_full_name = db.Column(db.String(length=50), nullable=False)
    contact_email = db.Column(db.String(length=50), nullable=True)
    contact_mobilephone = db.Column(db.String(length=50), nullable=True)
    date = db.Column(db.String(), default=datetime.date.today())


    def __repr__(self):
        return f' Candidat id : {self.user_id}'

    def json(self):
        return {
            'id': self.id, 
            'user_id': self.user_id, 
            'lien': self.lien,
            'poste': self.poste,
            'entreprise': self.entreprise,
            'activite': self.activite,
            'type': self.type,
            'lieu': self.lieu,
            'contact_full_name': self.contact_full_name,
            'contact_email': self.contact_email,
            'contact_mobilephone': self.contact_mobilephone,
            'date': self.date,
            }


    @classmethod
    def find_by_user_id(cls, user_id):
        offer_list=[]
        for offer in cls.query.filter_by(user_id=user_id).all():
            offer_list.append(offer.json())
        return jsonify(offer_list)

    @classmethod
    def get_all_in_list_with_user_name(cls):
        offer_list=[]
        for offer in cls.query.join(Users).with_entities(Users.first_name, cls.lien, cls.poste, cls.entreprise, cls.activite, cls.type, cls.lieu,  cls.contact_full_name, cls.contact_email, cls.contact_mobilephone, cls.date).all():
            offer_list.append(offer)
        return offer_list

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

# Function to create db and populate it
def init_db():
    db.drop_all()
    db.create_all()
    
    # Insert all users from  "static/liste_apprenants.csv"
    with open("App/static/liste_apprenants.csv", newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

   
    for i in data:
        user = {
                'email_address' : i[0],
                'first_name' : i[1],
                'last_name' : i[2],
                'password_hash' : generate_password_hash(i[3], method='sha256'),
                'is_admin' : True if i[4] == "TRUE" else False
            }
        Users(**user).save_to_db()
    
    lg.warning('Database initialized!')