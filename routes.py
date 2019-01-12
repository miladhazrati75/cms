import binascii
import hashlib
import os
from flask_sqlalchemy import SQLAlchemy
from flask import *

app = Flask(__name__)

app.secret_key = binascii.hexlify(os.urandom(32))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cms.db'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40), unique=True)
    name = db.Column(db.String(40), unique=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/Login')
def show_login():
    session['form'] = 'login'
    return render_template('auth.html')


@app.route('/ValidateLogin', methods=['GET', 'POST'])
def login():
    user = request.form['user']
    pwd = hashlib.sha1(request.form['pass'].encode('utf-8')).hexdigest()
    qlogin = User.query.filter(User.username == user, User.password == pwd).first()
    if qlogin is None:
        session['msg'] = 'Login Failed.'
    else:
        qlogin = User.query.filter(User.username == user, User.password == pwd).first()
        session['username'] = qlogin.username
        session['name'] = qlogin.name
        session['logged'] = True
        session['msg'] = 'Successful login.'
    return render_template('index.html', msg=session)


@app.route('/Logout')
def logout():
    del session['username']
    del session['logged']
    return render_template('index.html')


@app.route('/Register')
def show_register():
    session['form'] = 'register'
    return render_template('auth.html')


@app.route('/ValidateRegister', methods=['GET', 'POST'])
def register():
    user = request.form['user']
    pwd = hashlib.sha1(request.form['pass'].encode('utf-8')).hexdigest()
    name = request.form['name']
    h = User(username=user, password=pwd, name=name)
    db.session.add(h)
    db.session.commit()
    session['username'] = user
    session['logged'] = True
    session['name'] = request.form['name']
    session['msg'] = 'success!'
    return render_template('index.html', msg=session)


@app.route('/EditProfile')
def show_edit_profile():
    user = session['username']
    qfetchedit = User.query.filter(User.username == user).first()
    user = qfetchedit.username
    name = qfetchedit.name
    session['form'] = 'edit'
    return render_template('auth.html', edit=(user, name))


@app.route('/ValidateEdit', methods=['GET', 'POST'])
def edit_profile():
    qedit = User.query.filter(User.username == session['username']).first()
    qedit.username = request.form['user']
    pwd = hashlib.sha1(request.form['pass'].encode('utf-8')).hexdigest()
    qedit.name = request.form['name']
    db.session.commit()
    session['username'] = request.form['user']
    session['name'] = request.form['name']
    session['msg'] = 'Edit Done.'
    session['logged'] = True
    return render_template('index.html', msg=session)


if __name__ == '__main__':
    app.run(debug=True)
