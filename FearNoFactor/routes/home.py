from flask import render_template

from FearNoFactor import app, login_manager, person

from flask_login import login_required, current_user
from flask import request
from flask import redirect
from flask import url_for


# Flask-Login helper to retrieve a user from our db
from FearNoFactor.db import DBProxy
from FearNoFactor.routes.login import login
from FearNoFactor.routes.service import setLastMode


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
                           mode=mode, showModeToggle=True, email=current_user.email)

@app.route('/basic')
def basicMode():
    if not current_user.is_authenticated:
        base_url = request.base_url
        if base_url[-1] == '/':
            base_url = base_url[:-1]
        # remove /basic from url
        base_url = base_url[:-6]
        return login(f'{base_url}/login', 'basic')
    setLastMode(current_user.email, '0')  # 0=basic, 1=advanced. Must be string to simulate query parameter.
    return redirect(url_for('home'))

@app.route('/advanced')
def advancedMode():
    if not current_user.is_authenticated:
        base_url = request.base_url
        if base_url[-1] == '/':
            base_url = base_url[:-1]
        # remove /advanced from url
        base_url = base_url[:-9]
        return login(f'{base_url}/login', 'advanced')
    setLastMode(current_user.email, '1')  # 0=basic, 1=advanced. Must be string to simulate query parameter.
    return redirect(url_for('home'))

@app.route('/about')
@login_required
def about():
    return render_template('about.html', showModeToggle=False)


@app.route('/help')
@login_required
def help():
    return render_template('help.html', showModeToggle=False)