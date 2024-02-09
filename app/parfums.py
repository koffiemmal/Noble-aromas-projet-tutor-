from app.models import Parfum, Categorie
from sqlalchemy.sql.expression import func
def get_parfums_homme():
    return Parfum.query.filter_by(categorie_id=1).all()

def get_parfums_femme():
    return Parfum.query.filter_by(categorie_id=2).all()

def get_parfums_mixte():
    return Parfum.query.filter_by(categorie_id=3).all()
def random_products():
    return Parfum.query.order_by(func.random()).limit(3).all()
def get_all():
    return Parfum.query.all()

def acceuil():
    return Parfum.query.filter_by(categorie_id=4).order_by(func.random()).limit(1).all()

def acceuilsuite():
    return Parfum.query.filter_by(categorie_id=4).order_by(func.random()).limit(4).all()