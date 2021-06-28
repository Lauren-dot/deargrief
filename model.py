from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import TIMESTAMP
from app import login_manager
from login import UserMixin

db = SQLAlchemy()

@login_manager.bereaved_loader
def load_bereaved(bereaved_id):
    return Bereaved.query.get(int(bereaved_id))

class Bereaved(db.Model):
    """Data Model for a bereaved user"""
    __tablename__ = "bereaved_persons"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date_first_registered = db.Column(TIMESTAMP) 

    deceased_persons = db.relationship("Deceased", backref="bereaved") 

    def __repr__(self):
        """Show information about bereaved user"""

        greeting = f"Dear {self.firstname} {self.lastname}, thank you for engaging with your grief today."

        return greeting

class Deceased(db.Model):
    """Data Model for a deceased person"""
    __tablename__ = "deceased_persons"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    bereaved_id = db.Column(db.Integer, db.ForeignKey("bereaved_persons.id"), nullable=False)

    # See bereaved persons table for the relationship "backref" here.

    def __repr__(self):
        """Show information about bereaved user"""

        greeting = f"Dear {self.firstname} {self.lastname}, may your memory be a blessing."

        return greeting

class GriefConnection(db.Model):
    """Connection table: 
    Creating the specific, unique connection between one bereaved person and one deceased person"""

    __tablename__ = "grief_connection"
    
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    bereaved_id = db.Column(db.Integer, db.ForeignKey("bereaved_persons.id"), nullable=False)
    deceased_id = db.Column(db.Integer, db.ForeignKey("deceased_persons.id"), nullable=False)

    deceased_persons = db.relationship("Deceased", backref="bereaved")


class GriefSequence(db.Model):
    """Data Model to assess where a bereaved person 
    is in the cycle of this particuar grief with this particular loss"""
    __tablename__ = "grief_sequence"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    grief_connection_id = db.Column(db.Integer, db.ForeignKey("grief_connection.id"), nullable=False)
    prompt_series_id = db.Column(db.Integer, db.ForeignKey("prompt_series.id"), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.now) 
    status = db.Column(db.String(50), db.ForeignKey("UserGriefSequenceStatus.id"), nullable=False)
    most_recent_update = db.Column(db.DateTime, nullable=False)
    most_recent_day = db.Column(db.Integer, nullable=False) 

#   prompts = db.Relationship("Prompt Series", backref="")

    def __repr__(self):
        """Show which day of the grief sequence a bereaved person is"""

        greeting = f"Hello, you are on day {self.most_recent_day} of 60 in this process."

        return greeting


class SequenceStatus(db.Model):
    """Catalogues status of Grief Sequence.
    Examples: Active, Abandonded, Paused, Completed"""
    __tablename__ = "sequence_status"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    status_description = db.Column(db.Text, nullable=True)

# Ref: UserGriefSequenceStatus.id > UserGriefSequence.status #still unsure of correct syntax here. Just leaving a note it needs to be done
    
    def __repr__(self):
        """Show information about status regarding a particular journal 
        written by a bereaved person about a particular deceased person"""

        greeting = f"Hello, this journal is currently {self.status}."

        return greeting


class PromptSeries(db.Model):
    """Defines which grief sequence to use 
    (eg. kind of relationship between deceased and bereaved, 
    or other grief process"""
    __tablename__ = "prompt_series"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False) #Type of Grief (eg. Death, Change, Motherhood, Miscarriage)
    number_of_days = db.Column(db.Integer, nullable=False, default=60) 
    can_extend = db.Column(db.Boolean, nullable=False)
    can_pause = db.Column(db.Boolean, nullable=False)

    #human = db.relationship('Human', back_populates='animals')

    def __repr__(self):
        """Show information about which prompt series was chosen for this loss"""

        greeting = f"This particular journal is deals with grief associated with {self.name}."

        return greeting 


class Prompts(db.Model):
    """Information which will spark an entry from a bereaved person about a deceased person"""
    __tablename__ = "prompts"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    prompt_series_id = db.Column(db.Integer, db.ForeignKey("prompt_series.id"), nullable=False)
    day_number = db.Column(db.Integer, nullable=False)
    momentary_monitoring = db.Column(db.Integer, nullable=False)
    framing_quote = db.Column(db.Text, nullable=True)
    prompt = db.Column(db.Text, nullable=False)

    # Need syntax for: Ref: Prompts.prompt_series_id > PromptSeries.id

    def __repr__(self):
        """Show information about the prompts."""
        
        greeting = f"So happy that you are progressing through {self.day_number}. Your prompt is {self.prompt}."

        return greeting


class JournalEntry(db.Model):
    """The Journal Responses:
    Pairs unique bereaved-deceased grief connection with chosen prompt series and particular prompt for journal entry"""
    __tablename__ = "journal_entries"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    grief_connection_id = db.Column(db.Integer, db.ForeignKey("grief_connection.id"), nullable=False)
    prompt_series_id = db.Column(db.Integer, db.ForeignKey("prompt_series.id"), nullable=False)
    prompt_id = db.Column(db.Integer, db.ForeignKey("prompt.id"), nullable=False)
    prompt_day = db.Column(db.Integer, db.ForeignKey("prompt.day_number"), nullable=False)
    entry = db.Column(db.Text, nullable=False)

    #Consult on "backref", etc for all of this

    def __repr__(self):
        """Show information about each journal entry"""

        greeting = f"This particular journal entry is about day {self.prompt_day} of {self.bereaved_id}'s loss of {self.deceased_id}."

        return greeting
  

#Database Connection Infastructure 
#Adapted from model.py in sqlalchemy assessment
def connect_to_db(app):
    """Connect the database to our Flask app."""
    db.app = app
    db.init_app(app) #enables the db to read the hidden environment variables
    print("Connected to db!")


if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)
    connect_to_db(app)