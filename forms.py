import wtforms
from wtforms import Form, StringField, PasswordField
from wtforms.validators import Email, Length, EqualTo, InputRequired, DataRequired
from models import UserModel, EmailCaptchaModel
from exts import db

class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="Email format error!")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="Verification code format is wrong!")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="Username format error!")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="Please enter the password length between 6 to 20!")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="The password entered twice is inconsistent")])

    def validate_email(self, field):
        """Check whether the email address has been registered"""
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="This email address has already been registered!")

    def validate_captcha(self, field):
        """Check whether the verification code is correct"""
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="Email or verification code is wrong!")
            # TODO

class LoginForm(wtforms.Form):
    email= wtforms.StringField(validators=[Email(message="Email format error!")])
    password = wtforms.StringField(validators=[Length(min=6,max=20,message="Password format error!")])

class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3,max=100,message="Title format is wrong!")])
    content = wtforms.StringField(validators=[Length(min=3,message="Content format error!")])

class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3,message="Content format error!")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="The question id must be passed in!")])

    