from App import db
from .user import Users

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