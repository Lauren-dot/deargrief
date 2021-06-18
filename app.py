#Import the "Flask" class from the flask library
from flask import Flask, request, render_template, url_for, flash, redirect
from login import RegistrationForm, LogInForm
#Create the variable "app"; 
#Create an instance of the Flask class; 
#__name__ is a special variable in Python that represents the name of the module (it's so flask knows what to look for in static files, etc)
app = Flask(__name__) 
app.config["SECRET_KEY"] = "MAKE_SECRET_LATER"

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
    form = RegistrationForm() #Instance of the Registration Form (check login.py for class)
    if form.validate_on_submit():
        # Created the user in the database
        flash(f"Account created for {form.username.data}.", "success") #creates temp window with message; bootstrap class of message: success
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LogInForm() #Instance of the Log In Form (check login.py for class)
    #To DO
    #Process the form and log the user in
    #Redirect the User to their particular site/page

    return render_template("login.html", title="Log In", form=form)

#@app.route("/day/<calendar_counter>")
    #To Do
    #Match number of days to database containing the day-by-day prompts

    #Calendar counter corresponds to the index of days of journaling
    #Each calendar counter starts with a unique deceased and bereaved combination

    #return render_template("daily_journal_entry.html", prompts=prompts) 
    #when database "prompts" and html are ready, take out the first ) to access the database 
    #and be able to pass it to the html file

#To run flask directly
if __name__ == '__main__':
    #call "run" on our app
    app.run(debug=True) #running with the debug on means that it will hotload when you refresh