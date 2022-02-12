from flask import render_template, redirect, url_for, flash, request
from App import db, app
from forms import AddCandidacy, ModifyCandidacy
from datetime import datetime
from lclass import Candidacy, bot 
from flask_login import login_required, current_user
from tools import math_relance, count_alertes, notif_relance
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
            candidacy.modified_date = form.modified_date.data
            candidacy.status = form.status.data
            candidacy.relance = form.relance.data
            candidacy.date = form.date.data
            candidacy.modified_quand = datetime.now()
            db.session.commit()

            flash(f"La candidature a bien été modifiée",category="secondary")
            return redirect(url_for('board_page'))
        else:
            flash('Something goes wrong', category="danger")
    return render_template('modify_candidacy.html', form=form , candidacy=candidacy.json())
    
@app.route('/delete_candidacy')
def delete_candidacy():
    """[Allow to delete candidacy in the BDD with the id and redirect to board page]"""

    candidacy_id = request.args.get('id')
    Candidacy.query.filter_by(id=candidacy_id).first().delete_from_db()
    flash("Candidature supprimée avec succès",category="secondary")
    return redirect(url_for('board_page'))

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