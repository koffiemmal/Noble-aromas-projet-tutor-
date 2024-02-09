from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_url




app = Flask(__name__)
bcrypt = Bcrypt(app)

login_manager=LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

app.config['SECRET_KEY']="ShE_JJq4RJYoAANsbLk2Ig"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
db = SQLAlchemy(app)
Bootstrap(app)
from app import router
migrate = Migrate(app,db)



