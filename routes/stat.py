from flask import render_template
from App import app, lclass
from flask_login import login_required
import plotly.express as px
import plotly
import json as js
import pandas as pd

@app.route('/stat')
@login_required
def stat_page():
    df = pd.DataFrame(lcass.Candidacy.query.join(lclass.Users).with_entities(lclass.Users.first_name,lclass.Users.last_name,lclass.Users.email_address,lclass.Candidacy.status, lclass.Candidacy.entreprise).all(),columns=["first_name","last_name","mail","status","enterprise"])
    df["full_name"] = df["first_name"] + " " + df["last_name"]
    df["alternance"] = False
    df["alternance"].loc[df["status"]=="Alternance"] = True
    fig1 = px.histogram(df["full_name"])
    graphJSON1 = js.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    fig2 = px.pie(df[["mail","alternance"]].groupby(["mail"]).sum(),names="alternance")
    graphJSON2 = js.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('stat.html',graph1=graphJSON1, graph2=graphJSON2)