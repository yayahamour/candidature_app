from App import db
import datetime
from .user import Users
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
    contact_full_name = db.Column(db.String(length=50), nullable=True)
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