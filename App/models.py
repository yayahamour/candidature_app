
from App import db,login_manager, mail , app
import datetime 
from flask_login import UserMixin # allow to set variable is_active=True and to stay connected
import logging as lg
from werkzeug.security import generate_password_hash
import csv
from flask import jsonify
from dataclasses import dataclass, field 
from flask_mail import Mail , Message


@login_manager.user_loader
def load_user(user_id):
    """Allow to create a current_user with his id

    Args:
        user_id (int): user_id from the database

    Returns:
        instance of users depending of his id
    """
    return Users.query.get(int(user_id))

class Bot:

    def __init__(self, date_tchecker=[1]):
        self.date_tchecker = date_tchecker


    def mail_relance(self, adresse):
        
        jour = str(datetime.date.today())[8:]
        if str(self.date_tchecker[-1]) != jour:
            msg = Message(subject="Relance suivit candidature Simplon", 
                        body="Bonjour Apprenant, \nJe suis le bot créer par tes confrères et je suis là pour te rappeler que tu as des alertes de candidatures à relancer. \nVa vite faire un tour sur http://suivicandidature.herokuapp.com/",
                        sender=app.config.get("MAIL_USERNAME"),
                        recipients=[adresse])
            try: 
                #mail.send(msg)
                print('jour : ', jour)
                print('element liste all', self.date_tchecker )
                print('dernier element de la liste', self.date_tchecker[-1])
                print('-------------------   email envoyé! ------------------- \n')
            except:
                print('ERROR - Please tchek your email config')
            del self.date_tchecker[-1]
            self.date_tchecker.append(jour)
        else:
            print('Message Non envoyé')
    
    
    
bot = Bot()


class Users(db.Model,UserMixin):
    """Create a table Users on the candidature database

    Args:
        db.Model: Generates columns for the table
        UserMixin: Generates an easy way to provide a current_user

    """
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
    modified_date = db.Column(db.String(), default='-')
    modified_quand = db.Column(db.String(), default=datetime.date.today())
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
            'modified_date': self.modified_date,
            'status': self.status,
            'relance': self.relance
        }

    @classmethod
    def find_by_user_id(cls, user_id):
        candidacy_list = []
        for candidacy in cls.query.filter_by(user_id=user_id).all():
            candidacy_list.append(candidacy.json())
        return candidacy_list

    @classmethod
    def get_all_in_list_with_user_name(cls):
        candidacy_list=[]
        for candidacy in cls.query.join(Users).with_entities(Users.first_name, cls.plateforme, cls.poste, cls.entreprise, cls.activite, cls.type, cls.lieu,  cls.contact_full_name, cls.contact_email, cls.contact_mobilephone, cls.date, cls.status, cls.relance, cls.modified_date).all():
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


class Events(db.Model):
    """Create a table Events on the candidature database

    Args:
        db.Model: Generates columns for the table

    """

    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id'), nullable=False)
    event_title = db.Column(db.String(), nullable=False)
    start_date = db.Column(db.String(), nullable=False)
    end_date = db.Column(db.String(), nullable=False)
    url = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return f' Candidat id : {self.user_id}'

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_title': self.event_title,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'url': self.url
        }

    @classmethod
    def find_by_user_id(cls, user_id):
        event_list = []
        for event in cls.query.filter_by(user_id=user_id).all():
            event_list.append(event.json())
        return event_list

    @classmethod
    def get_all_in_list_with_user_name(cls):
        event_list = []
        for event in cls.query.join(Users).with_entities(Users.first_name, cls.event_title, cls.start_date, cls.end_date, cls.url).all():
            event_list.append(event)
        return event_list

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
    #db.session.add( )

    Users(last_name="ben", first_name= "charles", email_address= "cb@gmail.com", password_hash= generate_password_hash("1234", method='sha256'), is_admin=True).save_to_db() 
    Users(last_name="beniac", first_name= "cha", email_address= "bb@gmail.com", password_hash= generate_password_hash("1234", method='sha256'), is_admin=False).save_to_db()
    Candidacy(user_id = 2, entreprise = "facebook", contact_full_name = "mz", contact_email="mz@facebook.fb").save_to_db()
    Candidacy(user_id = 2, entreprise = "google", contact_full_name = "lp", contact_email="lp@gmail.com").save_to_db()
    Events(user_id=1, event_title='Test', start_date='08/02/2022',
           end_date='09/02/2022', url='').save_to_db()

    # Insert all users from  "static/liste_apprenants.csv"
    with open("App/static/liste_apprenants.csv", newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

   
    for i in data[6:]:
        user = {
                'email_address' : i[0],
                'first_name' : i[1],
                'last_name' : i[2],
                'password_hash' : generate_password_hash(i[3], method='sha256'),
                'promo' : "Dev Ia",
                'is_admin' : True if i[4] == "TRUE" else False
            }
        Users(**user).save_to_db()
    
    Candidacy(user_id = 2, entreprise = "facebook", contact_full_name = "mz", contact_email="mz@facebook.fb").save_to_db()
    Candidacy(user_id = 2, entreprise = "google", contact_full_name = "lp", contact_email="lp@gmail.com", status="Validée").save_to_db()
    Candidacy(user_id = 3, entreprise = "google", contact_full_name = "lp", contact_email="lp@gmail.com", status="Validée").save_to_db()
    Candidacy(user_id = 4, entreprise = "google", contact_full_name = "lp", contact_email="lp@gmail.com", status="Validée").save_to_db()
    Candidacy(user_id = 5, entreprise = "google", contact_full_name = "lp", contact_email="lp@gmail.com", status="Validée").save_to_db()
    Candidacy(user_id = 6, entreprise = "google", contact_full_name = "lp", contact_email="lp@gmail.com", status="Validée").save_to_db()    
    lg.warning('Database initialized!')
