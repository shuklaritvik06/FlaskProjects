from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class LoginForm(FlaskForm):
    username = StringField(label='username')
    password = StringField(label='password')
    submit = SubmitField(label='submit')
