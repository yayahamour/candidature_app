from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField, StringField, DateField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from .models import Users
from datetime import date, datetime


class Login(FlaskForm):
    """[Form to login]
    """
    email = EmailField(label="Adresse mail:", validators=[DataRequired()])
    password = PasswordField(label="Mot de passe:",
                             validators=[DataRequired()])
    submit = SubmitField(label="Se connecter")


class AddCandidacy(FlaskForm):
    """[Form to add candidacy]
    """
    entreprise = StringField(label='Entreprise', validators=[DataRequired()])
    contact_full_name = StringField(
        label='contact_full_name', validators=[DataRequired()])
    contact_email = StringField(
        label='contact_email', validators=[DataRequired()])
    contact_mobilephone = StringField(label='contact_mobilephone')
    submit = SubmitField(label='Ajouter')


class ModifyProfile(FlaskForm):
    """[Form to modify profile]
    """
    email = EmailField(label="Adresse mail:", validators=[DataRequired()])
    current_password = PasswordField(
        label="Mot de passe actuel:", validators=[DataRequired()])
    new_password = PasswordField(
        label="Nouveau mot de passe:", validators=[DataRequired()])
    submit = SubmitField(label="Valider")


class ModifyCandidacy(FlaskForm):
    """[form to modify candidacy]
    """
    contact_full_name = StringField(
        label='contact_full_name', validators=[DataRequired()])
    contact_email = StringField(
        label='contact_email', validators=[DataRequired()])
    contact_mobilephone = StringField(label='contact_mobilephone')
    status = StringField(label='Status', validators=[DataRequired()])
    modified_date = DateField('Modification Date', format='%Y-%m-%d')
    submit = SubmitField(label="Valider")


class AddEvent(FlaskForm):
    """[form to add events to Calender
    """
    event_title = StringField(label='Event title', validators=[DataRequired()])
    start_date = DateField(label='Start Date', format='%Y-%m-%d')
    end_date = DateField(label='End Date', format='%Y-%m-%d')
    url = StringField(label='Url')
    submit = SubmitField(label="Valider")
