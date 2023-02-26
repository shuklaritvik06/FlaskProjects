from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired


class RegisterForm(FlaskForm):
    username = StringField(label='username', validators=[Length(min=2, max=30)])
    password = PasswordField(label='password', validators=[DataRequired()])
    submit = SubmitField(label='submit')
