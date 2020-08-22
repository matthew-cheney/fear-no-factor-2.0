from FearNoFactor import db, person


def createPerson(person_in):
    db.session.add(person_in)
    db.session.commit()

def existsPerson(email):
    res = db.session.query(person).filter_by(email=email).first()
    return res is not None

def getPerson(email):
    return db.session.query(person).filter_by(email=email).first()

def addNumberAndIncrSolved(email, number, mode):
    res = db.session.query(person).filter_by(email=email).first()
    if mode == 0:
        res.next_easy_problem = number
        res.easy_problems_solved += 1
    else:
        res.next_hard_problem = number
        res.hard_problems_solved += 1
    db.session.commit()

def setMode(email, mode):
    res = db.session.query(person).filter_by(email=email).first()
    res.difficulty_left_off_on = mode
    db.session.commit()