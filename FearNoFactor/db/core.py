from FearNoFactor import db

def create(obj):
    db.session.add(obj)