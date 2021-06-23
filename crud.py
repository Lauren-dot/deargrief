"""CRUD (Create, Retrieve, Update, Delete) Data Functions"""

from model import Bereaved, Deceased, GriefConnection, GriefSequence, JournalEntry, SequenceStatus

"""Create"""

def create_bereaved(id, firstname, lastname, email, password, date_first_registered):
    """Create and return a bereaved person (user)"""

    bereaved = Bereaved(
        id=id,
        firstname=firstname,
        lastname=lastname,
        email=email,
        password=password,
        date_first_registered=date_first_registered,
    )

    db.session.add(bereaved)
    db.session.commit()

    return bereaved

def create_deceased(id, firstname, lastname, bereaved_id):
    """Create and return a deceased person"""

    deceased = Deceased(
        id=id,
        firstname=firstname,
        lastname=lastname,
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
    """Create: status of a particular grief connection 
    (For example: Active, Abandonded, Paused, Completed)"""

    sequence_status = SequenceStatus(
        id=id,
        status=status,
        status_description=status_description,
    )

    db.session.add(sequence_status)
    db.session.commit()

    return sequence_status


def create_journal_entries(id, grief_connection_id, prompt_series_id, prompt_id, prompt_day, entry):
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

# TO DO:
# def create_promptseries():

# TO DO:
# def create_grief_connection():




"""Connecting this to the rest of the app"""
if __name__ == '__main__':
    from server import app
    connect_to_db(app)