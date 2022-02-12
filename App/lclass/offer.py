from App import db
import datetime
from flask import jsonify
from .user import Users

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
    def get_all(cls):
        offer_list=[]
        for offer in cls.query.all():
            offer_list.append(offer.json())
        return offer_list

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