from asyncio import events
from flask import render_template, redirect, url_for, flash, request
from App import db, app
from datetime import date, datetime
from .models import Users, Candidacy, Events
from .forms import Login, AddCandidacy, ModifyCandidacy, ModifyProfile, AddEvent
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash


@app.route('/')
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
            flash(
                f"Vous êtes connecté en tant que : {user.first_name} {user.last_name}", category="success")
            return redirect(url_for('board_page'))
        else:
            flash('Adresse email ou mot de passe invalide', category="danger")
    return render_template('login.html', form=form)


@app.route('/board', methods=['GET', 'POST'])
@login_required
def board_page():
    """[Allow to generate the template of board.html on board path, if user is authenticated else return on login]

    Returns:
        [str]: [board page code different if the user is admin or not]
    """
    admin_candidacy_attributs = ["user_fisrt_name", 'entreprise',
                                 'contact_full_name', 'contact_email', 'contact_mobilephone', 'date', 'status']
    usercandidacy_attributs = ['entreprise', 'contact_full_name',
                               'contact_email', 'contact_mobilephone', 'date', 'modified date', 'status']

    if (current_user.is_admin == True):
        return render_template('board.html', lenght=len(admin_candidacy_attributs), title=admin_candidacy_attributs, user_candidacy=Candidacy.get_all_in_list_with_user_name())
    else:
        return render_template('board.html', lenght=len(usercandidacy_attributs), title=usercandidacy_attributs, user_candidacy=Candidacy.find_by_user_id(current_user.id))


@app.route('/logout')
def logout_page():
    """[Allows to disconnect the user and redirect to the home page]
    """
    logout_user()
    flash('Vous êtes correctement déconnecté', category="success")
    return redirect(url_for('home_page'))


@app.route('/candidature', methods=['GET', 'POST'])
def add_candidature():
    """[Allow to generate the template of add_candidacy.html on candidacy path to add candidacy in the BDD if validate and redirect to the board page when finish]

    Returns:
        [str]: [Candidacy code page]
    """
    form = AddCandidacy()
    if form.validate_on_submit():
        Candidacy(user_id=current_user.id, entreprise=form.entreprise.data, contact_full_name=form.contact_full_name.data,
                  contact_email=form.contact_email.data, contact_mobilephone=form.contact_mobilephone.data).save_to_db()
        flash('Nouvelle Candidature ajouté ', category='success')
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
            current_user.password_hash = generate_password_hash(
                form.new_password.data, method='sha256')
            db.session.add(current_user)
            db.session.commit()

            flash(f"Votre mot de passe a été modifié", category="success")
            return redirect(url_for('board_page'))
        else:
            flash('Adresse email ou mot de passe invalide', category="danger")
    return render_template('modify_profile.html', form=form)


@app.route('/modify_candidacy', methods=['GET', 'POST'])
@login_required
def modify_candidacy():
    """[Allow to generate the template of modify_candidacy.html on modify_candidacy path to modify candidacy in the BDD if validate and redirect to the board page when finish]

    Returns:
        [str]: [modify candidacy code page]
    """
    form = ModifyCandidacy()
    candidacy_id = request.args.get('id')
    candidacy = Candidacy.query.filter_by(id=candidacy_id).first()

    if form.validate_on_submit():

        if candidacy:
            candidacy.contact_full_name = form.contact_full_name.data
            candidacy.contact_email = form.contact_email.data
            candidacy.contact_mobilephone = form.contact_mobilephone.data
            candidacy.modified_date = form.modified_date.data
            candidacy.status = form.status.data
            candidacy.modified_quand = datetime.now()
            db.session.commit()

            flash(f"La candidature a bien été modifié", category="success")
            return redirect(url_for('board_page'))
        else:
            flash('Something goes wrong', category="danger")
    return render_template('modify_candidacy.html', form=form, candidacy=candidacy.json())


@app.route('/delete_candidacy')
def delete_candidacy():
    """[Allow to delete candidacy in the BDD with the id and redirect to board page]"""

    candidacy_id = request.args.get('id')
    Candidacy.query.filter_by(id=candidacy_id).first().delete_from_db()
    flash("Candidature supprimé avec succés", category="success")
    return redirect(url_for('board_page'))


<<<<<<< Updated upstream
<<<<<<< Updated upstream
@app.route('/cal')
=======
@app.route('/cal', methods=['GET', "POST"])
>>>>>>> Stashed changes
@login_required
def cal():
    """[Allow to generate the template of cal.html on calendar path, if user is authenticated else return on login]

    Returns:
        [str]: [the calender page returns the events saved to the calender]
    """
    form = AddEvent()
    if form.validate_on_submit():
        Events(user_id=current_user.id, event_title=form.event_title.data, start_date=form.start_date.data, end_date=form.end_date.data,
               url=form.url.data).save_to_db()
        flash('Nouvel événement ajouté.', category='success')
    event_attributes = ['event', 'start date', 'end date', 'url']
<<<<<<< Updated upstream
    return render_template('calender.html', events=Events.find_by_user_id(current_user.id))
=======
<<<<<<< Updated upstream
    notif_relance(count_alertes())
    
    app.jinja_env.globals.update(alertes = count_alertes())
    
    return render_template('relance.html', title = header, user_candidacy=Candidacy.find_by_user_id(current_user.id), math_relance=math_relance, body = body)

=======
@app.route('/cal', methods=['GET', "POST"])
@login_required
def cal():
    """[Allow to generate the template of cal.html on calendar path, if user is authenticated else return on login]

    Returns:
        [str]: [the calender page returns the events saved to the calender]
    """
    form = AddEvent()
    if form.validate_on_submit():
        Events(user_id=current_user.id, event_title=form.event_title.data, start_date=form.start_date.data, end_date=form.end_date.data,
               url=form.url.data).save_to_db()
        flash('Nouvel événement ajouté.', category='success')
    event_attributes = ['event', 'start date', 'end date', 'url']
    return render_template('calender.html', events=Events.find_by_user_id(current_user.id), form=form)
>>>>>>> Stashed changes
>>>>>>> Stashed changes
=======
    return render_template('calender.html', events=Events.find_by_user_id(current_user.id), form=form)
>>>>>>> Stashed changes


@app.route('/add', methods=['GET', "POST"])
@login_required
def add():
    form = AddEvent()
    if form.validate_on_submit():
        Events(user_id=current_user.id, event_title=form.event_title.data, start_date=form.start_date.data, end_date=form.end_date.data,
               url=form.url.data).save_to_db()
        flash('Nouvel événement ajouté.', category='success')
        return redirect(url_for('cal'))
    return render_template('add.html', form=form)
