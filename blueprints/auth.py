from flask import Blueprint, render_template, jsonify, redirect, url_for, session, flash, request
import random
import string
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import MultiDict
from models import EmailCaptchaModel, UserModel
from exts import mail, db
from flask_mail import Message
from .forms import RegisterForm, LoginForm
import logging
from flask_login import login_user, logout_user

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/about')
def about():
    return render_template('aboutUs.html')

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        data = request.get_json()
        form = LoginForm(formdata=MultiDict(data))
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                return jsonify({'success': False, 'message': 'Email does not exist.'})
            if check_password_hash(user.password, password):
                login_user(user)
                session['user_id'] = user.id
                return jsonify({'success': True}), 200
            else:
                return jsonify({'success': False, 'message': 'Incorrect password.'})
        else:
            errors = []
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f"Error in {field}: {error}")
            return jsonify({'success': False, 'message': ' '.join(errors)})

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("auth.login"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in {field}: {error}", "danger")
            return redirect(url_for("auth.register"))

@bp.route("/captcha/email", methods=['POST'])
def get_email_captcha():
    email = request.json.get("email")
    if not email:
        return jsonify({"code": 400, "message": "Email is required", "data": None})

    logging.info(f"Email received: {email}")

    try:
        source = string.digits
        captcha = ''.join(random.choices(source, k=4))

        message = Message(subject="Verification code", recipients=[email], body=f"Your verification code is {captcha}")
        mail.send(message)

        email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
        db.session.add(email_captcha)
        db.session.commit()

        return jsonify({"code": 200, "message": "", "data": None})
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"code": 500, "message": "Internal server error", "data": None})

@bp.route("/logout")
def logout():
    logout_user()
    session.pop('user_id', None)
    return redirect(url_for('qa.index'))
