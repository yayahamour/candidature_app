from flask import render_template, flash, redirect, url_for
from App import app
from werkzeug.security import check_password_hash
from forms import Login
from ..lclass import Users
from flask_login import login_user, logout_user

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

@app.route('/logout')
def logout_page():
    """[Allows to disconnect the user and redirect to the home page]
    """
    logout_user()
    flash('Vous êtes correctement déconnecté',category="secondary")
    return redirect(url_for('welcome_page'))