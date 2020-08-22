from FearNoFactor import app
from FearNoFactor import BASIC_LOWER, BASIC_UPPER, HARD_LOWER, HARD_UPPER
from FearNoFactor import person
from FearNoFactor.db import user as db_user
from FearNoFactor.db import DBProxy

import json
import random
from flask import jsonify
from flask import request
from FearNoFactor.utils import getFactors

@app.route('/api')
@app.route('/api/')
def apiHome():
    return "Hello, API!"

@app.route('/api/get-problem', methods=['POST'])
def getProblem():
    js = request.get_json(force=True)
    guessed_pairs = js.get('pairs')
    mode = js.get('mode')
    email = js.get('email')
    current_user = DBProxy.getPerson(email)
    target_num = (current_user.next_easy_problem if mode == 0 else current_user.next_hard_problem)
    if guessed_pairs is not None and {tuple(x) for x in guessed_pairs} == getFactors(target_num):
        if mode == 0:
            new_number = random.randint(BASIC_LOWER, BASIC_UPPER)
        else:
            new_number = random.randint(HARD_LOWER, HARD_UPPER)
        DBProxy.addNumberAndIncrSolved(current_user.email, new_number, mode)
    else:
        new_number = target_num
    return str(new_number)

@app.route('/api/get-total-passed/<email>/<mode>', methods=['GET'])
def getProblemsPassed(email, mode):
    current_user = DBProxy.getPerson(email)
    if mode == '0':
        return str(current_user.easy_problems_solved)
    else:
        return str(current_user.hard_problems_solved)

@app.route('/api/set-last-mode/<email>/<mode>', methods=['POST'])
def setLastMode(email, mode):
    current_user = DBProxy.getPerson(email)
    if mode == '0':
        DBProxy.setMode(current_user.email, 'basic')
    else:
        DBProxy.setMode(current_user.email, 'hard')
    return ''