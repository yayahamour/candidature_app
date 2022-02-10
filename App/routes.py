from ast import Try
from flask import render_template, redirect, url_for, flash, request
from sqlalchemy import JSON, false
from App import db, app
from datetime import date
from .models import Users, Candidacy, Offer, bot  
from .forms import Login, AddCandidacy, ModifyCandidacy, ModifyProfile, AddOffer, ModifyOffer , Stats
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import pandas as pd
import plotly
import plotly.express as px
import json
import numpy as np
from .tools import math_relance, count_alertes, notif_relance

@app.route('/')
@app.route('/welcome')
def welcome_page():
    """[Page for visitors before login]"""

    return render_template('welcome.html')

@app.route('/home')
def home_page():
    """[Allow to generate the template of home.html on home path]

    Returns:
        [str]: [home page code]
    """
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """[Allow to ask login and generate the template of login.html on login path]

    Returns:
        [str]: [login page code]
    """
    form = Login()
    if form.validate_on_submit():
        user = Users.query.filter_by(email_address=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash(f"Vous êtes connecté en tant que : {user.first_name} {user.last_name} - promotion : {user.promo} {user.year}",category="secondary")
            return redirect(url_for('board_page'))
        else:
            flash('Adresse email ou mot de passe invalide',category="danger")
    return render_template('login.html',form=form)




@app.route('/board', methods=['GET','POST'])
@login_required
def board_page():
    """[Allow to generate the template of board.html on board path, if user is authenticated else return on login]

    Returns:
        [str]: [board page code different if the user is admin or not]
    """

    admin_candidacy_attributs = ["Apprenant",'plateforme', 'poste','entreprise', 'activite', 'type', 'lieu', 'Nom du contact','Email du contact', 'Téléphone du contact' ,'date','statut']
    usercandidacy_attributs = ['plateforme','poste','entreprise', 'activite', 'type', 'lieu','Nom du contact','Email du contact', 'Téléphone du contact' ,'date','statut']
    app.jinja_env.globals.update(alertes = count_alertes())


    if (current_user.is_admin == True):  
        return render_template('board.html', lenght = len(admin_candidacy_attributs), title = admin_candidacy_attributs, user_candidacy=Candidacy.get_all_in_list_with_user_name())
    else:
        return render_template('board.html', lenght = len(usercandidacy_attributs), title = usercandidacy_attributs ,user_candidacy=Candidacy.find_by_user_id(current_user.id))


@app.route('/logout')
def logout_page():
    """[Allows to disconnect the user and redirect to the home page]
    """
    logout_user()
    flash('Vous êtes correctement déconnecté',category="secondary")
    return redirect(url_for('welcome_page'))

@app.route('/candidature', methods= ['GET', 'POST'])
def add_candidature():
    """[Allow to generate the template of add_candidacy.html on candidacy path to add candidacy in the BDD if validate and redirect to the board page when finish]

    Returns:
        [str]: [Candidacy code page]
    """
    form = AddCandidacy()
    if form.validate_on_submit():
        Candidacy(user_id = current_user.id, plateforme = form.plateforme.data, poste = form.poste.data, entreprise = form.entreprise.data, activite = form.activite.data, type = form.type.data, lieu = form.lieu.data, contact_full_name = form.contact_full_name.data, contact_email = form.contact_email.data, contact_mobilephone = form.contact_mobilephone.data).save_to_db()
        flash('Nouvelle Candidature ajoutée ', category='secondary')
        return redirect(url_for('board_page'))
    return render_template('add_candidacy.html', form=form)

@app.route('/modify_profile', methods=['GET', 'POST'])
@login_required
def modify_profile():
    """[Allow to generate the template of modify_profile.html on modify_profile path to modify profile in the BDD if validate and redirect to the board page when finish]

    Returns:
        [str]: [modify profile code page]
    """
    form = ModifyProfile()
    if form.validate_on_submit():
        if current_user.email_address == form.email.data and check_password_hash(current_user.password_hash, form.current_password.data):
            current_user.password_hash = generate_password_hash(form.new_password.data, method='sha256')
            db.session.add(current_user)
            db.session.commit()

            flash(f"Votre mot de passe a été modifié",category="secondary")
            return redirect(url_for('board_page'))
        else:
            flash('Adresse email ou mot de passe invalide',category="danger")
    return render_template('modify_profile.html',form=form)

@app.route('/modify_candidacy', methods=['GET', 'POST'])
@login_required
def modify_candidacy():
    """[Allow to generate the template of modify_candidacy.html on modify_candidacy path to modify candidacy in the BDD if validate and redirect to the board page when finish]

    Returns:
        [str]: [modify candidacy code page]
    """
    form = ModifyCandidacy()
    candidacy_id = request.args.get('id')
    candidacy = Candidacy.query.filter_by(id = candidacy_id).first()
    
    if form.validate_on_submit():
        
        if candidacy:
            candidacy.plateforme = form.plateforme.data
            candidacy.poste = form.poste.data
            candidacy.entreprise = form.entreprise.data
            candidacy.activite = form.activite.data
            candidacy.type = form.type.data
            candidacy.lieu = form.lieu.data
            candidacy.contact_full_name = form.contact_full_name.data
            candidacy.contact_email = form.contact_email.data
            candidacy.contact_mobilephone = form.contact_mobilephone.data
            candidacy.status = form.status.data
            candidacy.relance = form.relance.data
            candidacy.date = form.modif_date.data
            db.session.commit()

            flash(f"La candidature a bien été modifiée",category="secondary")
            return redirect(url_for('board_page'))
        else:
            flash('Something goes wrong',category="danger")
    return render_template('modify_candidacy.html', form=form , candidacy=candidacy.json())
    
@app.route('/delete_candidacy')
def delete_candidacy():
    """[Allow to delete candidacy in the BDD with the id and redirect to board page]"""

    candidacy_id = request.args.get('id')
    Candidacy.query.filter_by(id=candidacy_id).first().delete_from_db()
    flash("Candidature supprimée avec succès",category="secondary")
    return redirect(url_for('board_page'))

@app.route('/visualisation')
def visualisation_page():
    """[Show differents visualizations]"""

    cnx = sqlite3.connect('app.db')
    df = pd.read_sql_query("SELECT * FROM candidacy", cnx)

    fig_avancement = px.pie(df, names='status', title ='Répartition des candidatures de la promo par : avancement des candidatures')
    graphavancement = json.dumps(fig_avancement, cls=plotly.utils.PlotlyJSONEncoder)

    fig_metiers = px.pie(df, names='poste', title ='Répartition des candidatures de la promo par : métiers visés')
    graphmetier = json.dumps(fig_metiers, cls=plotly.utils.PlotlyJSONEncoder)

    fig_activite = px.pie(df, names='activite', title ="Répartition des candidatures de la promo par : secteurs d'activité")
    graphactivite = json.dumps(fig_activite, cls=plotly.utils.PlotlyJSONEncoder)

    fig_type = px.pie(df, names='type', title ="Répartition des candidatures de la promo par : type d'entreprise")
    graphtype = json.dumps(fig_type, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('visualisation.html', graphavancement = graphavancement, graphmetier=graphmetier, graphactivite=graphactivite, graphtype=graphtype)


@app.route('/offres', methods=['GET','POST'])
@login_required
def offres_page():
    """[Show differents job offers], if user is authenticated else return on login]

    Returns:
        [str]: [board page code different if the user is admin or not]
    """

    offer_attributs = ['poste','entreprise', 'activite', 'type', 'lieu', 'Nom du contact','Email du contact', 'Téléphone du contact' ,'date']

    return render_template('offres.html', lenght = len(offer_attributs), title = offer_attributs, user_offer=Offer.get_all())
 

@app.route('/add_offer', methods= ['GET', 'POST'])
def add_offer():
    """[Allow to generate the template of add_offer.html on candidacy path to add offer in the BDD if validate and redirect to the board page when finish]

    Returns:
        [str]: [Candidacy code page]
    """
    form = AddOffer()
    if form.validate_on_submit():
        Offer(user_id = current_user.id, lien = form.lien.data, poste = form.poste.data, entreprise = form.entreprise.data, activite = form.activite.data, type = form.type.data, lieu = form.lieu.data, contact_full_name = form.contact_full_name.data, contact_email = form.contact_email.data, contact_mobilephone = form.contact_mobilephone.data).save_to_db()
        flash("Nouvelle offre d'emploi ajoutée", category='secondary')
        return redirect(url_for('offres_page'))
    return render_template('add_offer.html', form=form)

@app.route('/add_to_candidacy')
def add_to_candidacy():
    """[Add an offer to a candadicies list]"""

    # form = AddOffer()
    # if form.validate_on_submit():
    #     Candidacy(user_id = current_user.id, plateforme = "Offre de l'appli", poste = form.poste.data, entreprise = form.entreprise.data, activite = form.activite.data, type = form.type.data, lieu = form.lieu.data, contact_full_name = form.contact_full_name.data, contact_email = form.contact_email.data, contact_mobilephone = form.contact_mobilephone.data).save_to_db()
    #     flash('Nouvelle Candidature ajoutée ', category='secondary')
    #     return redirect(url_for('board_page'))
    # return render_template('add_candidacy.html', form=form)
    return 'En cours'


@app.route('/modify_offer', methods=['GET', 'POST'])
@login_required
def modify_offer():
    """[Allow to generate the template of modify_offer.html on modify_candidacy path to modify offer in the BDD if validate and redirect to the board page when finish]

    Returns:
        [str]: [modify candidacy code page]
    """
    form = ModifyOffer()
    offer_id = request.args.get('id')
    offer = Offer.query.filter_by(id = offer_id).first()

    if form.validate_on_submit():
        
        if offer:
            offer.lien = form.lien.data
            offer.poste = form.poste.data
            offer.entreprise = form.entreprise.data
            offer.activite = form.activite.data
            offer.type = form.type.data
            offer.lieu = form.lieu.data
            offer.contact_full_name = form.contact_full_name.data
            offer.contact_email = form.contact_email.data
            offer.contact_mobilephone = form.contact_mobilephone.data
            db.session.commit()

            flash(f"L'offre d'emploi a bien été modifiée",category="secondary")
            return redirect(url_for('offres_page'))
        else:
            flash('Something goes wrong',category="danger")
    return render_template('modify_offer.html', form=form , offer=offer.json())

@app.route('/delete_offer')
def delete_offer():
    """[Allow to delete offer in the BDD with the id and redirect to board page]"""

    offer_id = request.args.get('id')
    Offer.query.filter_by(id=offer_id).first().delete_from_db()
    flash("Offre d'emploi supprimée avec succès",category="secondary")
    return redirect(url_for('offres_page'))

@app.route('/relaunch')
def relaunch_page():
    """[Show which candidacies need relaunch]"""

    return render_template('relaunch.html')

@app.route('/calendar')
def calendar_page():
    """[Show the calendar]"""

    return render_template('calendar.html')

@app.route('/profil')
def profil_page():
    """[Show some elements of the user]"""

    return render_template('profil.html')

@app.route('/gestion')
def gestion_page():
    """[To add/modify/delete profiles]"""

    userlist_attributs = ['Nom', 'Prénom', 'Email', 'Téléphone', 'promotion', 'année', 'CV', 'Droits']

    if (current_user.is_admin == True):  
        return render_template('gestion.html', lenght = len(userlist_attributs), title = userlist_attributs, user_list=Users.get_all())

@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return gm(request.args.get('data'))

@app.route('/scallback', methods=['POST', 'GET'])
def tp():
    return list_fonction(request.args.get('data'))
   
@app.route('/stats')
@login_required
def stats():
    form = Stats()
    list_learner = Users.get_all_learner()
    option_select = []
    for learner in list_learner:
        if learner[1] not in option_select:
            option_select.append(learner[1])
    form.promo = option_select
    return render_template('graph.html',form=form, list_option=option_select)

def list_fonction(vue = "all"):
    print(vue)
    if(vue == "all"):
        list_learner = Users.get_all_learner()
    else:
        list_learner = Users.find_by_promo(vue)
    list_no_apprenticeship = str()
    list_have_apprenticeship = str()
    for learner in list_learner:
        list_candidacy = Candidacy.find_by_user_id(learner[0])
        apprenticeship = False
        for candidacy in list_candidacy :
            if candidacy["status"] == "Validée":
                apprenticeship = True
        if (apprenticeship) == True:
            if (len(list_have_apprenticeship) == 0):
                list_have_apprenticeship += str((Users.find_by_title(learner[0])))
            else:
                list_have_apprenticeship += ";" + str((Users.find_by_title(learner[0])))
            
        else:
            if (len(list_no_apprenticeship) == 0):
                list_no_apprenticeship += str((Users.find_by_title(learner[0])))
            else:
                list_no_apprenticeship += ";" + str((Users.find_by_title(learner[0])))
    return(json.dumps(list_have_apprenticeship + "|" + list_no_apprenticeship))
    
def gm(vue = "all"):
   
    if(vue == "all"):
        list_learner = Users.get_all_learner()
    else:
        list_learner = Users.find_by_promo(vue)
    df = pd.DataFrame()
    list_apprenticeship = []
    list_status = []
    for learner in list_learner:
        list_candidacy = Candidacy.find_by_user_id(learner[0])
        apprenticeship = False
        status = "En cours"
        for candidacy in list_candidacy :
            if candidacy["status"] == "Validée":
                apprenticeship = True
                status = "Validée"
        list_status.append(status)
        list_apprenticeship.append(apprenticeship)
    df["apprenticeship"] = list_apprenticeship
    df["status"] = list_status
    df = df.groupby("status").count().reset_index()
    
    fig = px.pie(df, values='apprenticeship', names ='status', title='Pourcentage alternance')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/relance') 
def relance_page():
    header = ['entreprise','contact_full_name','contact_email', 'contact_mobilephone' ,'Dernière relance', 'A relancer dès le', 'A été relancé']
    body = ['entreprise', 'contact_full_name', 'contact_email', 'contact_mobilephone' , 'date', 'relance' ]
    
    adresse = current_user.email_address
    notif_relance(count_alertes())
    # A importer pour ne pas instancier à chaque envois d'email. Voir pour en faire une table ? 
    # tchek = tcheker([]) 
    if count_alertes() > 0:
        bot.mail_relance(adresse)
    
    app.jinja_env.globals.update(alertes = count_alertes())
    return render_template('relance.html', title = header, user_candidacy=Candidacy.find_by_user_id(current_user.id), math_relance=math_relance, body = body)


