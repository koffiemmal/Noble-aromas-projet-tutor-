from app import db
from flask_login import UserMixin

utilisateur_categories = db.Table('utilisateur_categories',
    db.Column('utilisateur_id', db.Integer, db.ForeignKey('utilisateur.id'), primary_key=True),
    db.Column('categorie_id', db.Integer, db.ForeignKey('categorie.id'), primary_key=True)
)

class Utilisateur(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), unique=False, nullable=False)
    prenom = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(50), unique=False, nullable=False)
    admin = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    historique_commandes = db.relationship('Commande', backref='utilisateur', lazy=True)
    categories = db.relationship('Categorie', secondary=utilisateur_categories, lazy=True)

    def __repr__(self):
        return f'Utilisateur(nom={self.nom})'

class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    parfums = db.relationship('Parfum', backref='categorie', lazy=True)

class Parfum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    prix = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'), nullable=False)
    @classmethod
    def get_parfums_homme(cls):
        return cls.query.filter_by(categorie_id=1).all()
    @classmethod
    def get_parfums_femme(cls):
        return cls.query.filter_by(categorie_id=2).all()
    @classmethod
    def get_parfums_mixte(cls):
        return cls.query.filter_by(categorie_id=3).all()

class Commande(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Float, nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)

    def __repr__(self):
        return f'Commande(date={self.date})'