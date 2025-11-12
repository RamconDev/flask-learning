from app.main import main_bp as main

from flask import render_template, redirect, url_for

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')

@main.route('/register')
def register():
    return render_template('register.html')

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/logout')
def logout():
    return redirect( url_for('main.index') )