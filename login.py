# This is one option for the login form
from flask_wtf import FlaskForm #the library from flask that streamlines dealing with forms
from wtforms import StringField, PasswordField, SubmitField, BooleanField #the kinds of fields we are using
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError #These are all classes from the wtforms library; they make checking the form easier
from model import Bereaved
import re

class RegistrationForm(FlaskForm): #uses FlaskForm (imported above) to create a new class that we will use here
    #this next line will create and lable in the html a text field and then set up requirements for that field (eg: DataRequired tests if the field has any entry into it)
    firstname = StringField(
                    "First Name", 
                    validators=[
                        DataRequired(), 
                        Length(min=2, max=50)])
    lastname = StringField(
                    "Last Name", 
                    validators=[
                        DataRequired(), 
                        Length(min=2, max=50)])
    email = StringField(
                    "Email", 
                    validators=[
                        DataRequired(), 
                        Email()])
    password = PasswordField(
                    "Password", 
                    validators=[
                        DataRequired(), 
                        Length(min=8, max=100),
                        Regexp(
                            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z]).{8,15}$", #this is a regular expression! It is asking for any lower case, any uppercase, any numbers, and any characters that are not any of those!
                            message="Please make your password more secure by including upper and lower case letters, numbers, and special characters.")
                    ]
                )
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        #Checks that email is unique.
        bereaved_email = Bereaved.query.filter_by(email=email.data).first()
        if bereaved_email:
            raise ValidationError("An account already exists with this email. Please log in or try another email to register.")

class LogInForm(FlaskForm):
    email = StringField(
        "Email", 
        validators=[
            DataRequired(), 
            Email()])
    password = PasswordField(
        "Password", 
        validators=[
            DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class NewJournalForm(FlaskForm): #uses FlaskForm (imported above) to create a new class that we will use here
    #this next line will create and lable in the html a text field and then set up requirements for that field (eg: DataRequired tests if the field has any entry into it)
    firstname = StringField(
                    "First Name of Deceased", 
                    validators=[
                        DataRequired(), 
                        Length(min=2, max=50)])
    lastname = StringField(
                    "Last Name of Deceased", 
                    validators=[
                        DataRequired(), 
                        Length(min=2, max=50)])
    relationship = StringField(
                    "Your relationship with the Deceased", 
                    validators=[
                        DataRequired(), 
                        Length(min=2, max=100)])
    submit = SubmitField("Create")