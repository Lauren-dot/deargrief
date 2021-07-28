
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#from sqlalchemy.dialects.postgresql import TIMESTAMP <-- Not for MVP

from flask_login import UserMixin

db = SQLAlchemy()

class Bereaved(db.Model, UserMixin):
    """Data Model for a bereaved user"""
    __tablename__ = "bereaved_persons"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    #date_first_registered = db.Column(TIMESTAMP) <-- Not for MVP: Make sure to impliment across the board

    deceased_persons = db.relationship("Deceased", secondary="grief_connection", backref="bereaved_persons") 

    def __repr__(self):
        """Show information about bereaved user"""

        greeting = f"<<{self.firstname} {self.lastname} is in mourning."

        return greeting


class Deceased(db.Model):
    """Data Model for a deceased person"""
    __tablename__ = "deceased_persons"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    griefrelationship = db.Column(db.String(100), nullable=False)

    # See bereaved persons table for the relationship "backref" here.
    # See grief connection table for connection table "backref"

    def __repr__(self):
        """Show information about bereaved user"""

        greeting = f"<<{self.firstname} {self.lastname} is dead."

        return greeting



class GriefConnection(db.Model):
    """Connection table: 
    Creating the specific, unique connection between one bereaved person and one deceased person"""

    __tablename__ = "grief_connection"
    
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    bereaved_id = db.Column(db.Integer, db.ForeignKey("bereaved_persons.id"), nullable=False)
    deceased_id = db.Column(db.Integer, db.ForeignKey("deceased_persons.id"), nullable=False)
    # deceased_persons = db.relationship("Deceased", backref="grief_connection")
    # bereaved_person = db.relationship("Bereaved", backref="grief_connection")

    def __repr__(self):
        """Show connection between the bereaved and deceased"""

        greeting = f"<<{self.bereaved_person} is grieving {self.deceased_persons}" 

        return greeting


class GriefSequence(db.Model):
    """Data Model to assess where a bereaved person 
    is in the cycle of this particuar grief with this particular loss"""
    __tablename__ = "grief_sequence"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    grief_connection_id = db.Column(db.Integer, db.ForeignKey("grief_connection.id"), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.now) 
    most_recent_update = db.Column(db.DateTime, nullable=False)
    most_recent_day = db.Column(db.Integer, autoincrement=True, nullable=False) 

    grief_connection = db.relationship("GriefConnection", backref="grief_sequence")

    def __repr__(self):
        """Show which day of the grief sequence a bereaved person is"""

        greeting = f"Hello, you are on day {self.most_recent_day} of 60 in this process."

        return greeting


class Prompts(db.Model):
    """Information which will spark an entry from a bereaved person about a deceased person"""
    __tablename__ = "prompts"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    day_number = db.Column(db.Integer, nullable=False)
    momentary_monitoring = db.Column(db.String, nullable=False)
    prompt = db.Column(db.Text, nullable=False)


    def __repr__(self):
        """Show information about the prompts."""
        
        greeting = f"<<On {self.day_number}. Your prompt is {self.prompt}."

        return greeting


class JournalEntry(db.Model):
    """The Journal Responses:
    Pairs unique bereaved-deceased grief connection with chosen prompt series and particular prompt for journal entry"""
    __tablename__ = "journal_entries"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    grief_connection_id = db.Column(db.Integer, db.ForeignKey("grief_connection.id"), nullable=False)
    prompt_day = db.Column(db.Integer, nullable=False)
    momentary_monitoring = db.Column(db.Integer, nullable=False)
    entry = db.Column(db.Text, nullable=False)

    #Consult on how to connect this:
    #grief_connection = db.relationship("GriefConnection", backref="journal_entries")

    def __repr__(self):
        """Show information about each journal entry"""

        greeting = f"<<Concerning day {self.prompt_day} of {self.bereaved_id}'s loss of {self.deceased_id}."

        return greeting
  

#Database Connection Infastructure 
#Adapted from model.py in sqlalchemy assessment
def connect_to_db(app):
    """Connect the database to our Flask app."""
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///DearGriefDatabase"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app) #enables the db to read the hidden environment variables
    print("Connected to db!")

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    db.create_all()
    #call "run" on our app
    # app.run(debug=True)

