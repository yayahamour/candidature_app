from flask import render_template, redirect, url_for, flash, request
from App import db, app
from ..forms import AddOffer, ModifyOffer
from models import Offer
from flask_login import login_required, current_user

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
