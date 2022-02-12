from flask import render_template, request
from App import app
from .forms import Stats
from lclass import Users, Candidacy
from flask_login import login_required
import pandas as pd
import plotly
import plotly.express as px
import json

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