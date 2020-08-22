from flask import render_template

from FearNoFactor import app, login_manager, person

from flask_login import login_required, current_user


# Flask-Login helper to retrieve a user from our db
from FearNoFactor.db import DBProxy


@login_manager.user_loader
def load_user(email):
    return DBProxy.getPerson(email)

@app.route('/public')
def public():
    return render_template('public.html', showModeToggle=False)

@app.route('/')
@login_required
def home():
    if current_user.difficulty_left_off_on == 'basic':
        mode = 0
        problems_passed = current_user.easy_problems_solved
    else:
        mode = 1
        problems_passed = current_user.hard_problems_solved
    return render_template('factoringGround.html', totalProblemsPassed=problems_passed,
                           mode=mode, showModeToggle=True)

@app.route('/about')
@login_required
def about():
    return render_template('about.html', showModeToggle=False)


@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html', showModeToggle=False)