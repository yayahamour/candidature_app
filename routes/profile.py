from flask import render_template

@app.route('/profile/')
@login_required
def profile_page():

    return render_template('profile.html')