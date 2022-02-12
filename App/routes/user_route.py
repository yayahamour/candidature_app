from flask import render_template, redirect, url_for, flash, request
from App import db, app
from ..forms import AddUser, ModifyUser, ModifyProfile
from ..lclass import Users
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

@app.route('/add_user', methods= ['GET', 'POST'])
def add_user():
    """[To add an user to the database]

    Returns:
        [str]: [User code page]
    """

    form = AddUser()
    if form.validate_on_submit():
        Users(last_name = form.last_name.data, first_name = form.first_name.data, email_address = form.email_address.data, password_hash = generate_password_hash(form.password_hash.data, method='sha256'), telephone_number = form.telephone_number.data, promo = form.promo.data, year = form.year.data, curriculum = form.curriculum.data, is_admin = form.is_admin.data).save_to_db()
        flash('Nouvel utilisateur ajouté ', category='secondary')
        return redirect(url_for('gestion_page'))
    return render_template('add_user.html', form=form)

@app.route('/modify_user', methods=['GET', 'POST'])
@login_required
def modify_user():
    """[Allow to generate the template of modify_candidacy.html on modify_candidacy path to modify candidacy in the BDD if validate and redirect to the board page when finish]

    Returns:
        [str]: [modify candidacy code page]
    """
    form = ModifyUser()
    user_id = request.args.get('id')
    user = Users.query.filter_by(id = user_id).first()
    
    if form.validate_on_submit():
        
        if user:
            user.last_name = form.last_name.data
            user.first_name = form.first_name.data
            user.email_address = form.email_address.data
            user.telephone_number = form.telephone_number.data
            user.promo = form.promo.data
            user.year = form.year.data
            user.curriculum = form.curriculum.data
            user.is_admin = form.is_admin.data
            db.session.commit()

            flash(f"L'utilisateur' a bien été modifié",category="secondary")
            return redirect(url_for('gestion_page'))
        else:
            flash('Something goes wrong',category="danger")
    return render_template('modify_user.html', form=form , user=user)

@app.route('/delete_user')
def delete_user():
    """[Allow to delete candidacy in the BDD with the id and redirect to board page]"""

    user_id = request.args.get('id')
    Users.query.filter_by(id=user_id).first().delete_from_db()
    flash("Utilisateur supprimé avec succès",category="secondary")
    return redirect(url_for('gestion_page'))

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