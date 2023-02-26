from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired, ValidationError
from ..models.model import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_check):
        user = User.query.filter_by(username=username_check.data).first()
        if user:
            raise ValidationError("User already exists")

    username = StringField(label='username', validators=[Length(min=2, max=30)])
    password = PasswordField(label='password', validators=[DataRequired()])
    submit = SubmitField(label='submit')
