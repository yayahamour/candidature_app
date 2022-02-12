from App import db,login_manager
from flask_login import UserMixin


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
    promo = db.Column(db.String(length=30), nullable=True)
    year = db.Column(db.String(length=20), nullable=True)
    curriculum = db.Column(db.String(), nullable=True)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self):
        return f'{self.last_name} {self.first_name}'

    def json(self):
        return {
            'id' : self.id,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'email_address': self.email_address,
            'telephone_number': self.telephone_number,
            'promo' : self.promo,
            'year': self.year,
            'curriculum': self.curriculum,
            'is_admin': self.is_admin
        }

    @classmethod
    def find_by_title(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def get_all(cls):
        user_list=[]
        for info in cls.query.all():
            user_list.append(info.json())
        return user_list

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

@login_manager.user_loader
def load_user(user_id):
    """Allow to create a current_user with his id

    Args:
        user_id (int): user_id from the database

    Returns:
        instance of users depending of his id
    """
    return Users.query.get(int(user_id))