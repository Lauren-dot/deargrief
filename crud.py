"""CRUD (Create, Retrieve, Update, Delete) Data Functions"""

from model import Bereaved, Deceased, GriefConnection, GriefSequence, JournalEntry, PromptSeries, Prompts, SequenceStatus
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

"""Create"""

def create_bereaved(id, firstname, lastname, email, password, date_first_registered):
    """Create and return a bereaved person (user)"""

#Uncomment this once you have restructured your code into packages - it's throwing errors because there is too much cross-section working
#     hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8") #.decode turns this into a string (instead of dealing with bytes)
    
    bereaved = Bereaved(
        id=id,
        firstname=firstname,
        lastname=lastname,
        email=email,
        password=hashed_password,
        date_first_registered=date_first_registered,
    )

    db.session.add(bereaved)
    db.session.commit()

    return bereaved

def create_deceased(id, firstname, lastname, relationship, bereaved_id):
    """Create and return a deceased person"""

    deceased = Deceased(
        id=id,
        firstname=firstname,
        lastname=lastname,
        relationship=relationship,
        bereaved_id=bereaved_id,
    )

    db.session.add(deceased)
    db.session.commit()

    return deceased

def create_grief_connection(id, bereaved_id, deceased_id):
    """Create and return an identifiable connection 
    between a bereaved user and a deceased person 
    for whom the bereaved is grieving"""

    grief_connection = GriefConnection(
        id=id,
        bereaved_id=bereaved_id,
        deceased_id=deceased_id,
    )

    db.session.add(grief_connection)
    db.session.commit()

    return grief_connection

def create_grief_sequence(id, grief_connection_id, prompt_series_id, start_date, status, most_recent_update, most_recent_day):
    """Create: where a bereaved person is in a particular grief process"""

    grief_sequence = GriefSequence(
        id=id, 
        grief_connection_id=grief_connection_id, 
        prompt_series_id=prompt_series_id, 
        start_date=start_date, 
        status=status, 
        most_recent_update=most_recent_update, 
        most_recent_day=most_recent_day,
    )

    db.session.add(grief_sequence)
    db.session.commit()

    return grief_sequence


def create_grief_sequence_status(id, status, status_description):
    """Create and return status of a particular grief connection 
    (For example: Active, Abandonded, Paused, Completed)"""

    sequence_status = SequenceStatus(
        id=id,
        status=status,
        status_description=status_description,
    )

    db.session.add(sequence_status)
    db.session.commit()

    return sequence_status

def create_prompt_series(id, name, number_of_days, can_extend, can_pause):
    """Create and return different prompt series"""

    prompt_series = PromptSeries(
        id=id, 
        name=name, 
        number_of_days=number_of_days, 
        can_extend=can_extend, 
        can_pause=can_pause,
    )

    db.session.add(prompt_series)
    db.session.commit()

    return prompt_series


def create_prompts(id, prompt_series_id, day_number, momentary_monitoring, framing_quote, prompt):
    """Create and return prompts"""

    prompt = Prompts(
        id=id, 
        prompt_series_id=prompt_series_id, 
        day_number=day_number, 
        momentary_monitoring=momentary_monitoring, 
        framing_quote=framing_quote, 
        prompt=prompt,
    )

    db.session.add(prompt)
    db.session.commit()

    return prompt



def create_journal_entry(id, grief_connection_id, prompt_series_id, prompt_id, prompt_day, entry):
    """Create and return a user/bereaved's journal entry about a specific deceased person"""

    journal_entry = JournalEntry(
        id=id,
        grief_connection=grief_connection_id, 
        prompt_series_id=prompt_series_id, 
        prompt_id=prompt_id, 
        prompt_day=prompt_day, 
        entry=entry,
    )

    db.session.add(journal_entry)
    db.session.commit()

    return journal_entry


"""Retrieve"""
def get_bereaved_by_email(email):
    """Return a bereaved user by their email."""
     
    return Bereaved.query.get(Bereaved.email == email)

def get_deceased_by_user():
    pass

def get_journal_entry_by_day():
    pass


#Fix This
"""Connecting this to the rest of the app"""
if __name__ == '__main__': # If I am executing this file directly with python (python crud.py)
    from app import app
    connect_to_db(app)