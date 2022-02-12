from App import db, lclass
from .App.lclass.user import Users

def init_db():
    db.session.commit()
    db.drop_all()
    db.create_all()

    Users(last_name="ben", first_name= "charles", email_address= "cb@gmail.com", password_hash= generate_password_hash("1234", method='sha256'), is_admin=True).save_to_db()
    
