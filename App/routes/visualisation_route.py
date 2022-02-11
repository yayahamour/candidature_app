from flask import render_template
from App import app
from ..models import Users, Candidacy, Offer
from flask_login import login_required, current_user
import sqlite3
import pandas as pd
import plotly
import plotly.express as px
import json
from ..tools import count_alertes

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

@app.route('/profil')
def profil_page():
    """[Show some elements of the user]"""

    return render_template('profil.html')

@app.route('/gestion')
def gestion_page():
    """[To add/modify/delete profiles]"""

    userlist_attributs = ['Nom', 'Prénom', 'Email', 'Téléphone', 'promotion', 'année', 'Droits']
    if (current_user.is_admin == True):  
        return render_template('gestion.html', lenght = len(userlist_attributs), title = userlist_attributs, user_list=Users.get_all())
