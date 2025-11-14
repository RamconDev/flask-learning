# flask db migrate -m "Creación de modelo User"
# flask db upgrade

from app.main import main_bp as main

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.main.forms import RegistrationForm, LoginForm
from app import db

from app.models import User
from sqlalchemy import or_

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("Ya te has logueado!")
        return redirect( url_for('main.index') )
    
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User.create_user(
            name = form.name.data,
            email = form.email.data,
            username = form.username.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash("Registro exitoso!")
        return redirect( url_for('main.index') )

    return render_template('register.html',  form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("Ya te has logueado")
        return redirect( url_for('main.index') )
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter(
            or_(
                User.username == form.user_email.data,
                User.email == form.user_email.data
            ))).scalar_one_or_none()

        if not user or not user.check_password(form.password.data):
            flash("Datos invalidaos")
            return redirect( url_for("main.login") )
        
        login_user(user, form.stay_loggedin.data)

        next_page = request.args.get('next')

        return redirect( next_page or url_for("main.index") )

    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect( url_for('main.index') )

@main.route('/users')
@login_required
def users_list():
    users = db.session.execute(
        db.select(User).order_by(User.username)
    ).scalars().all()

    return render_template("users_list.html", users=users)