# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField , SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class AddPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(max=1000)])
    study_minutes = IntegerField("Study Minutes", validators=[NumberRange(min=0)])
    tags = StringField("Tags")
    submit = SubmitField("Add Post")


class SignUpForm(FlaskForm):
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired(), Length(max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
    submit = SubmitField("Sign Up")


class SignInForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class AboutUserForm(FlaskForm):
    # 表示専用なのでバリデーションは不要
    firstname = StringField("First Name")
    lastname = StringField("Last Name")
    username = StringField("Username")
    email = StringField("Email")
