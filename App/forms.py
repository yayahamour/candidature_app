from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField, StringField, DateField, BooleanField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from wtforms.fields import DateField, SelectField
from .models import Users
from datetime import date, datetime


class Login(FlaskForm):
    """[Form to login]
    """
    email = EmailField(label="Adresse mail:", validators=[DataRequired()])
    password = PasswordField(label="Mot de passe:",
                             validators=[DataRequired()])
    submit = SubmitField(label="Se connecter")

class AddUser(FlaskForm):
    """[Form to add user]
    """
    last_name = StringField(label='Nom', validators=[DataRequired()])
    first_name = StringField(label='Prénom', validators=[DataRequired()])
    email_address = StringField(label='Email', validators=[DataRequired()])
    password_hash = StringField(label='Mot de passe', validators=[DataRequired()])
    telephone_number = StringField(label='Téléphone')
    promo = StringField(label='Promotion')
    year = StringField(label='Année')
    curriculum = StringField(label='Lien du CV')
    is_admin = BooleanField(' Droits administrateur : ')
    submit = SubmitField(label='Ajouter')

class ModifyUser(FlaskForm):

    last_name = StringField(label='Nom', validators=[DataRequired()])
    first_name = StringField(label='Prénom', validators=[DataRequired()])
    email_address = StringField(label='Email', validators=[DataRequired()])
    telephone_number = StringField(label='Téléphone')
    promo = StringField(label='Promotion')
    year = StringField(label='Année')
    curriculum = StringField(label='CV')
    is_admin = BooleanField(' Droits administrateur : ')
    submit = SubmitField(label="Valider")
class AddCandidacy(FlaskForm):
    """[Form to add candidacy]
    """
    plateforme = StringField(label='Plateforme(Indeed, spontanée...)', validators=[DataRequired()])
    poste = SelectField(label='Poste', validators=[DataRequired()], choices = ['Data Analyst', 'Data Scientist','Data Engineer', 'Dev Ia', 'Dev Python'])
    entreprise = StringField(label='Entreprise', validators=[DataRequired()])
    activite = SelectField(label='Activité', validators=[DataRequired()], choices = ['Industrie', 'Marketing','Medecine', 'Autre'])
    type = SelectField(label='Type', validators=[DataRequired()], choices = ['Cabinet Conseil', 'Grand Groupe','Start-up'])
    lieu = StringField(label='Lieu', validators=[DataRequired()])
    contact_full_name = StringField(label='Nom du contact')
    contact_email = StringField(label='Email du contact')
    contact_mobilephone = StringField(label='Téléphone du contact')
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
    plateforme = StringField(label='Plateforme(Indeed, spontanée...)', validators=[DataRequired()])
    poste = SelectField(label='Poste', validators=[DataRequired()], choices = ['Data Analyst', 'Data Scientist','Data Engineer', 'Dev Ia', 'Dev Python'])
    entreprise = StringField(label='Entreprise', validators=[DataRequired()])
    activite = SelectField(label='Activité', validators=[DataRequired()], choices = ['Industrie', 'Marketing','Medecine', 'Autre'])
    type = SelectField(label='Type', validators=[DataRequired()], choices = ['Cabinet Conseil', 'Grand Groupe','Start-up'])
    lieu = StringField(label='Lieu', validators=[DataRequired()])
    contact_full_name = StringField(label='Nom du contact')
    contact_email = StringField(label='Email du contact')
    contact_mobilephone = StringField(label='Téléphone du contact')
    status = SelectField(label='Statut', validators=[DataRequired()], choices = ['En cours', 'A été relancée',"En attente d'entretien", "Acceptée", "Refusée"])
    date = DateField('Date de création', format='%Y-%m-%d')
    modified_date = DateField('Date de modification', format='%Y-%m-%d')
    relance = BooleanField('A été relancé ? ')
    submit = SubmitField(label="Valider")


class AddEvent(FlaskForm):
    """[form to add events to Calender
    """
    event_title = StringField(label='Event title', validators=[DataRequired()])
    start_date = DateField(label='Start Date', format='%Y-%m-%d')
    end_date = DateField(label='End Date', format='%Y-%m-%d')
    url = StringField(label='Url')
    submit = SubmitField(label="Valider")
    
    

class AddOffer(FlaskForm):
    """[Form to add offer]
    """
    lien = StringField(label="Lien de l'offre")
    poste = SelectField(label='Poste', validators=[DataRequired()], choices = ['Data Analyst', 'Data Scientist','Data Engineer', 'Dev Ia', 'Dev Python'])
    entreprise = StringField(label='Entreprise', validators=[DataRequired()])
    activite = SelectField(label='Activité', validators=[DataRequired()], choices = ['Industrie', 'Marketing','Medecine', 'Autre'])
    type = SelectField(label='Type', validators=[DataRequired()], choices = ['Cabinet Conseil', 'Grand Groupe','Start-up'])
    lieu = StringField(label='Lieu', validators=[DataRequired()])
    contact_full_name = StringField(label='Nom du contact')
    contact_email = StringField(label='Email du contact')
    contact_mobilephone = StringField(label='Téléphone du contact')
    submit = SubmitField(label='Ajouter')

class ModifyOffer(FlaskForm):
    """[form to modify offer]
    """

    contact_full_name = StringField(label='Nom du contact')
    contact_email = StringField(label='Email du contact')
    contact_mobilephone = StringField(label='Téléphone du contact')
    
    lien = StringField(label="Lien de l'offre")
    poste = SelectField(label='Poste', validators=[DataRequired()], choices = ['Data Analyst', 'Data Scientist','Data Engineer', 'Dev Ia', 'Dev Python'])
    entreprise = StringField(label='Entreprise', validators=[DataRequired()])
    activite = SelectField(label='Activité', validators=[DataRequired()], choices = ['Industrie', 'Marketing','Medecine', 'Autre'])
    type = SelectField(label='Type', validators=[DataRequired()], choices = ['Cabinet Conseil', 'Grand Groupe','Start-up'])
    lieu = StringField(label='Lieu', validators=[DataRequired()])
    submit = SubmitField(label="Valider")
    

class Stats(FlaskForm):
    promo =  SelectField('promo', choices=[])
   
    submit = SubmitField(label="Valider")
