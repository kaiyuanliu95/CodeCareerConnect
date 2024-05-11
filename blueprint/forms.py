from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import UserModel, EmailCaptchaModel
from exts import db

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=3, max=20, message="Username must be between 3 and 20 characters!")])
    email = StringField('Email', validators=[Email(message="Invalid email format!")])
    password = PasswordField('Password', validators=[Length(min=6, max=20, message="Password must be between 6 and 20 characters!")])
    password_confirm = PasswordField('Confirm Password', validators=[EqualTo('password', message="Passwords must match!")])
    submit = SubmitField('Register')

    def validate_email(self, field):
        """Check if the email has already been registered."""
        if UserModel.query.filter_by(email=field.data).first():
            raise ValidationError("This email is already registered!")

    def validate_captcha(self, field):
        """Check if the captcha is correct and linked to the email."""
        captcha_model = EmailCaptchaModel.query.filter_by(email=self.email.data, captcha=field.data).first()
        if not captcha_model:
            raise ValidationError("Invalid captcha or email!")
        # Optionally, delete the captcha record after verification
        db.session.delete(captcha_model)
        db.session.commit()

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email(message="Invalid email format!")])
    password = PasswordField('Password', validators=[Length(min=6, max=20, message="Password must be between 6 and 20 characters!")])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class QuestionForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=3, max=100, message="Title must be between 3 and 100 characters!")])
    content = StringField('Content', validators=[Length(min=3, message="Content must be at least 3 characters long!")])

class AnswerForm(FlaskForm):
    content = StringField('Content', validators=[Length(min=3, message="Content must be at least 3 characters long!")])
    question_id = IntegerField('Question ID', validators=[DataRequired(message="Question ID is required!")])
