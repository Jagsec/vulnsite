from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

username = getenv('USERNAME')
password = getenv('PASSWORD')
host = getenv('HOST')
database = getenv('DATABASE')
secret_key = getenv('SECRET')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{username}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secret_key

db = SQLAlchemy(app)

csrf = CSRFProtect()
csrf.init_app(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'loginPage'
login_manager.login_message_category = 'info'

from interface.routes.userRoutes import loginPage, logoutPage, registerPage, profilePage, editProfilePage
from interface.routes.challengeRoutes import challengePage
from interface.routes.globalRoutes import homePage, notFoundPage, notAuthenticatedPage
app.register_error_handler(404, notFoundPage)
app.register_error_handler(401, notAuthenticatedPage)