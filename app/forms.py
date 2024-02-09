from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,DateField,EmailField,TextAreaField,SelectField,IntegerField
from wtforms.validators import DataRequired,Length,Email
from wtforms.widgets import PasswordInput
from app.models import Categorie

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()],render_kw={'placeholder':"Entrez votre email :"})
    password = PasswordField('Password',validators=[DataRequired()],render_kw={'placeholder':"Entrez votre password :"})
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class UserForm(FlaskForm):
    nom = StringField('Nom',validators=[DataRequired(),Length(min=2,max=20)],render_kw={'placeholder':"Entrez votre nom :"})
    prenom = StringField('Prenom',validators=[DataRequired(),Length(min=2,max=20)],render_kw={'placeholder':"Entrez votre prenom :"})
    email = StringField('Email',validators=[DataRequired(),Email()],render_kw={'placeholder':"Entrez votre email :"})
    password = PasswordField('Password',render_kw={'placeholder':"Entrez votre password :"},widget=PasswordInput(hide_value=False))
    submit = SubmitField('Sign in')

class CategorieForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()],render_kw={'placeholder':"Entrez le nom de la categorie :"})
    description = TextAreaField('Description', validators=[DataRequired()],render_kw={'placeholder':"Entrez la description de la categorie :"})
    submit = SubmitField('Créer')

class ParfumForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()],render_kw={'placeholder':"Entrez le nom :"})
    description = TextAreaField('Description', validators=[DataRequired()],render_kw={'placeholder':"Entrez la description :"})
    prix = IntegerField('Prix', validators=[DataRequired()],render_kw={'placeholder':"Entrez le prix :"})
    image = StringField('Image', validators=[DataRequired()])
    categorie_id = SelectField('Catégorie', coerce=int)
    submit = SubmitField('Créer')

    def __init__(self, *args, **kwargs):
        super(ParfumForm, self).__init__(*args, **kwargs)
        self.categorie_id.choices = [(categorie.id, categorie.nom) for categorie in Categorie.query.all()]