from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm
from .models import db, User
from flask_mail import Message
from exts import mail
import random
import string

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        # Check if the email is already registered
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email already exists.', 'warning')
            return redirect(url_for('auth.register'))
        # Create new user with hashed password
        new_user = User(username=form.username.data, email=form.email.data,
                        password=generate_password_hash(form.password.data, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        # Authenticate the user
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/captcha/email', methods=['GET'])
def get_email_captcha():
    email = request.args.get("email")
    captcha = ''.join(random.choices(string.digits, k=4))  # Generate a 4-digit captcha
    message = Message(subject="Your Verification Code", recipients=[email], body=f"Your captcha is {captcha}")
    mail.send(message)
    # Here, add captcha to the database or a temporary store
    # Assuming EmailCaptchaModel exists and manages captcha
    db.session.add(EmailCaptchaModel(email=email, captcha=captcha))
    db.session.commit()
    return jsonify({"code": 200, "message": "Captcha sent successfully", "data": None})

@auth.route('/mail/test')
def mail_test():
    message = Message(subject="Email Test", recipients=["example@example.com"], body="This is a test email.")
    mail.send(message)
    return "Email sent successfully"
