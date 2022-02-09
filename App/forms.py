from flask_wtf import FlaskForm
from wtforms import PasswordField,EmailField,SubmitField,StringField
from wtforms.validators import Length,DataRequired,Email,EqualTo,ValidationError
from wtforms.fields import SelectField
from .models import Users

class Login(FlaskForm):
    """[Form to login]
    """
    email = EmailField(label="Adresse mail:", validators = [DataRequired()])
    password = PasswordField(label="Mot de passe:", validators = [DataRequired()])
    submit = SubmitField(label="Se connecter")


class AddCandidacy(FlaskForm):
    """[Form to add candidacy]
    """
    plateforme = StringField(label='Plateforme', validators=[DataRequired()])
    poste = SelectField(label='Poste', validators=[DataRequired()], choices = ['Data Analyst', 'Data Scientist','Data Engineer'])
    entreprise = StringField(label='Entreprise', validators=[DataRequired()])
    activite = SelectField(label='Activité', validators=[DataRequired()], choices = ['Industrie', 'Marketing','Medecine', 'Autre'])
    type = SelectField(label='Type', validators=[DataRequired()], choices = ['Cabinet Conseil', 'Grand Groupe','Start-up'])
    lieu = StringField(label='Lieu', validators=[DataRequired()])
    contact_full_name = StringField(label='Nom du contact', validators=[DataRequired()])
    contact_email = StringField(label='Email du contact', validators=[DataRequired()])
    contact_mobilephone = StringField(label='Téléphone du contact')
    submit = SubmitField(label='Ajouter')

class ModifyProfile(FlaskForm):
    """[Form to modify profile]
    """
    email = EmailField(label="Adresse mail:", validators = [DataRequired()])
    current_password = PasswordField(label="Mot de passe actuel:", validators = [DataRequired()])
    new_password = PasswordField(label="Nouveau mot de passe:", validators = [DataRequired()])
    submit = SubmitField(label="Valider")

class ModifyCandidacy(FlaskForm):
    """[form to modify candidacy]
    """
    plateforme = StringField(label='Plateforme', validators=[DataRequired()])
    poste = SelectField(label='Poste', validators=[DataRequired()], choices = ['Data Analyst', 'Data Scientist','Data Engineer'])
    entreprise = StringField(label='Entreprise', validators=[DataRequired()])
    activite = SelectField(label='Activité', validators=[DataRequired()], choices = ['Industrie', 'Marketing','Medecine', 'Autre'])
    type = SelectField(label='Type', validators=[DataRequired()], choices = ['Cabinet Conseil', 'Grand Groupe','Start-up'])
    lieu = StringField(label='Lieu', validators=[DataRequired()])
    contact_full_name = StringField(label='Nom du contact', validators=[DataRequired()])
    contact_email = StringField(label='Email du contact', validators=[DataRequired()])
    contact_mobilephone = StringField(label='Téléphone du contact')
    status = SelectField(label='Statut', validators=[DataRequired()], choices = ['En cours', 'A été relancée',"En attente d'entretien", "Acceptée", "Refusée"])

    submit = SubmitField(label="Valider")


class AddOffer(FlaskForm):
    """[Form to add offer]
    """
    lien = StringField(label="Lien de l'offre", validators=[DataRequired()])
    poste = SelectField(label='Poste', validators=[DataRequired()], choices = ['Data Analyst', 'Data Scientist','Data Engineer'])
    entreprise = StringField(label='Entreprise', validators=[DataRequired()])
    activite = SelectField(label='Activité', validators=[DataRequired()], choices = ['Industrie', 'Marketing','Medecine', 'Autre'])
    type = SelectField(label='Type', validators=[DataRequired()], choices = ['Cabinet Conseil', 'Grand Groupe','Start-up'])
    lieu = StringField(label='Lieu', validators=[DataRequired()])
    contact_full_name = StringField(label='Nom du contact', validators=[DataRequired()])
    contact_email = StringField(label='Email du contact', validators=[DataRequired()])
    contact_mobilephone = StringField(label='Téléphone du contact')
    submit = SubmitField(label='Ajouter')

class ModifyOffer(FlaskForm):
    """[form to modify offer]
    """
    lien = StringField(label="Lien de l'offre", validators=[DataRequired()])
    poste = SelectField(label='Poste', validators=[DataRequired()], choices = ['Data Analyst', 'Data Scientist','Data Engineer'])
    entreprise = StringField(label='Entreprise', validators=[DataRequired()])
    activite = SelectField(label='Activité', validators=[DataRequired()], choices = ['Industrie', 'Marketing','Medecine', 'Autre'])
    type = SelectField(label='Type', validators=[DataRequired()], choices = ['Cabinet Conseil', 'Grand Groupe','Start-up'])
    lieu = StringField(label='Lieu', validators=[DataRequired()])
    contact_full_name = StringField(label='Nom du contact', validators=[DataRequired()])
    contact_email = StringField(label='Email du contact', validators=[DataRequired()])
    contact_mobilephone = StringField(label='Téléphone du contact')
    
    submit = SubmitField(label="Valider")