import random
from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db, mail
from models import UserModel, EmailCaptchaModel
from .forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, current_user, login_required

bp = Blueprint('auth', __name__)

def generate_verification_code():
    return ''.join(random.choices('0123456789', k=6))

@bp.route('/send_code', methods=['POST'])
def send_code():
    email = request.json.get('email')
    code = generate_verification_code()
    expiration = datetime.utcnow() + timedelta(minutes=10)

    verification_code = EmailCaptchaModel.query.filter_by(email=email).first()
    if verification_code:
        verification_code.code = code
        verification_code.expiration = expiration
    else:
        verification_code = EmailCaptchaModel(email=email, code=code, expiration=expiration)
        db.session.add(verification_code)
    
    db.session.commit()

    msg = Message('Your Verification Code', sender='2849115967@qq.com', recipients=[email])
    msg.body = f'Your verification code is {code}. It will expire in 10 minutes.'
    mail.send(msg)

    return jsonify({'message': 'Verification code sent.'})
    
    
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        data = request.get_json()
        form = RegisterForm(data=data)
        if form.validate_on_submit():
            code = form.code.data
            verification_code = EmailCaptchaModel.query.filter_by(email=form.email.data).first()
            if not verification_code or verification_code.is_expired() or verification_code.code != code:
                return jsonify({'success': False, 'message': 'Invalid or expired verification code'}), 400
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            user = UserModel(username=form.username.data, email=form.email.data, password=hashed_password)
            try:
                db.session.add(user)
                db.session.commit()
                return jsonify({'success': True}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'success': False, 'message': 'An error occurred while creating your account. Please try again.'}), 500
        else:
            return jsonify({'success': False, 'message': 'Form validation failed. Please check the provided information.'}), 400
    return render_template('register.html', form=form)
    
    
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        data = request.get_json()
        print("Received data:", data)  

        form = LoginForm(data=data)
        if form.validate_on_submit():
            print("Form validation succeeded.")  
            print("Email from form:", form.email.data)  
            print("Password from form:", form.password.data)  

            user = UserModel.query.filter_by(email=form.email.data).first()
            if user:
                print("User found in database:", user)  
                password_check = check_password_hash(user.password, form.password.data)
                print("Password check result:", password_check)  

                if password_check:
                    login_user(user)
                    print("User logged in successfully.")  
                    return jsonify({'success': True}), 200
                else:
                    print("Password check failed.")  
                    return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
            else:
                print("User not found.")  
                return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        else:
            print("Form validation failed. Errors:", form.errors)  
            return jsonify({'success': False, 'message': 'Form validation failed. Please check the provided information.'}), 400
    print("Rendering login template.")  
    return render_template('login.html', form=form)
    

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('qa.index'))
    
@bp.route('/about')
def about():
    return render_template('aboutUs.html')  