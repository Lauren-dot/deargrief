#Import the "Flask" class from the flask library
import secrets
import random 
import os

from flask_sqlalchemy import SQLAlchemy
#from deargrief.basiccrud import create_deceased
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager #, login_user, current_user, logout_user, login_required
from deargrief.basicmodel import db, connect_to_db
#from crud import create_deceased, create_bereaved, create_journal_entry

#Create the variable "app"; 
#Create an instance of the Flask class; 
#__name__ is a special variable in Python that represents the name of the module (it's so flask knows what to look for in static files, etc)
# app = Flask(__name__) 
# secret_key = secrets.token_hex(16)
# app.config["SECRET_KEY"] = secret_key
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
# db = SQLAlchemy(app)

# bcrypt = Bcrypt(app)

# login_manager = LoginManager(app)
# login_manager.login_view = "login"
# login_manager.login_message_category = "info" #assigns these type of flashed message to the Bootstrap "Info" category (Makes a cleaner message!)

# from deargrief import routes

# connect_to_db(app)
# db.create_all()