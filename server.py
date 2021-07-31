from basicmodel import GriefConnection
import secrets
import os
from flask import Flask, request, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from prompts import prompts

app = Flask(__name__) 
secret_key = secrets.token_hex(16)
app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")


bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info" #assigns these type of flashed message to the Bootstrap "Info" category (Makes a cleaner message!)


#Tells the browser what to do when the client requests the "/" (root) page; And! Two routes can be handled by the same function
@app.route("/")
@app.route("/home")
def greeting():

    return render_template("home.html") #Tells computer to look in the "template" folder in this directory for a file that matches the file inside the ()


@app.route("/about")
def about():

    return render_template("about.html", title="About")


@app.route("/process")
def process():

    return render_template("process.html", title="Process")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("An account already exists for this email; please log in.")
        return redirect("/login")

    form = RegistrationForm() #Instance of the Registration Form (check login.py for class)

    #Note: I migragted and integrated the guts of my "create_bereaved" function here; it was not connecting consistently when I called it from crud.py
    if form.validate_on_submit():
        password = form.password.data
        #hashed_password = Bcrypt.generate_password_hash(form.password.data).decode("utf-8") #.decode turns this into a string (instead of dealing with bytes)
        #bcrypt.check_password_hash(hashed_password, form.password.data)

        bereaved = Bereaved(
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        email=form.email.data,
                        password=password, # use =hashed_password after debugging
                        )

        db.session.add(bereaved)
        db.session.commit()
        # Created the user in the database

        flash("Welcome! Your account has been created. Please log in!", "success") 
        return redirect("/login")

    return render_template("new_user_register.html", title="Register", form=form)


@login_manager.user_loader
def load_bereaved(bereaved_id):
    return Bereaved.query.get(int(bereaved_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/my_account")
    form = LogInForm() #Instance of the Log In Form (check forms.py for class)
    if form.validate_on_submit():
        bereaved = Bereaved.query.filter_by(email=form.email.data).first()
        password = Bereaved.query.filter_by(password=form.password.data).first()
        if bereaved and password: # After MVP: use Bcrypt.check_password_hash(bereaved.password, form.password.data): after debugging password hashing
            login_user(bereaved, remember=form.remember.data)
            return redirect("/my_account")
        else:
            flash("Oh no! That did not work. Please check your email and password.")
    return render_template("login.html", title="Log In", form=form)


@app.route("/my_account")
@login_required
def welcome_to_main_account():

    return render_template("my_account.html", grief_connections=current_user.grief_connections)


@app.route("/new_journal_registration", methods=["GET", "POST"])
@login_required
def register_new_journal():
    form = NewJournalForm()
    print("************")
    print()
    print()
    print(current_user)
    print(current_user.id)
    print()
    print()
    print("************")
    if form.validate_on_submit():
        deceased = Deceased(
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        griefrelationship=form.griefrelationship.data,
                        )
        print("************")
        print()
        print()
        print(deceased)
        print()
        print()
        print("************")
        db.session.add(deceased)
        db.session.commit()

        grief_connection = GriefConnection(
                            bereaved_id=current_user.id, 
                            deceased_id=deceased.id,
                        )
        db.session.add(grief_connection)
        db.session.commit()
        
        # current_user.deceased_persons.append(deceased)
        # db.session.commit()

        flash("Your new grief process has been started. Thank you for taking the next step on your path.", "success")
        return render_template("my_account.html", grief_connections=current_user.grief_connections)

    return render_template("new_journal_registration.html", title="New Journal Registration", form=form)


@app.route("/daily_journal_entry/<int:grief_connection_id>", methods=["GET", "POST"])
@login_required
def new_entry(grief_connection_id):

    last_entry=JournalEntry.query.filter_by(grief_connection_id=grief_connection_id).order_by(db.desc(JournalEntry.id)).first()
    if last_entry:
        prompt_day = last_entry.prompt_day
    else:
        prompt_day = 0

    form = NewEntryForm()
    if form.validate_on_submit():
        entry = JournalEntry(
                        grief_connection_id=grief_connection_id,
                        prompt_day=prompt_day+1,
                        momentary_monitoring=form.momentary_monitoring.data,
                        entry=form.entry.data,
                        )
        db.session.add(entry)
        db.session.commit()

        # current_user.journal_entries.append(entry)
        # db.session.commit()
        print("************")
        print()
        print()
        print("Hello!")
        print()
        print()
        print("************")

        flash("Your entry has been recorded. Thank you for taking one more step on your grief journey.", "succes")
        return render_template("my_account.html", grief_connections=current_user.grief_connections)
    return render_template("daily_journal_entry.html", form=form, prompt=prompts[prompt_day], last_entry=last_entry)


@app.route("/previous_journal_entries/<int:grief_connection_id>", methods=["GET", "POST"])
@login_required
def gather_previous_entries(grief_connection_id):

    previous_entries=JournalEntry.query.filter_by(grief_connection_id=grief_connection_id).all()

    return render_template("previous_journal_entries.html", grief_connections=current_user.grief_connections, prompt=prompts, previous_entries=previous_entries)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/home")

#To run flask directly
if __name__ == '__main__':
    from basicmodel import Bereaved, Deceased, JournalEntry, connect_to_db, db
    from forms import RegistrationForm, LogInForm, NewJournalForm, NewEntryForm
    connect_to_db(app)
    #call "run" on our app
    app.run(debug=True) #running with the debug on means that it will hotload when you refresh