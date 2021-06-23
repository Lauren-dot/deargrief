"""CRUD (Create, Retrieve, Update, Delete) Data Functions"""

# def create_movie(title, overview, release_date, poster_path):
#     """Create and return a new movie."""

#     movie = Movie(
#         title=title,
#         overview=overview,
#         release_date=release_date,
#         poster_path=poster_path,
#     )

#     db.session.add(movie)
#     db.session.commit()

#     return movie

from model import Bereaved, Deceased, JournalEntry


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