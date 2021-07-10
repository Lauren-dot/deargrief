#from deargrief import app
from flask import Flask
import secrets
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from deargrief.basicmodel import connect_to_db

app = Flask(__name__) 
secret_key = secrets.token_hex(16)
app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info" #assigns these type of flashed message to the Bootstrap "Info" category (Makes a cleaner message!)

connect_to_db(app)
db.create_all()

#To run flask directly
if __name__ == '__main__':
    #call "run" on our app
    app.run(debug=True) #running with the debug on means that it will hotload when you refresh