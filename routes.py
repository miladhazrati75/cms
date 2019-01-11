from flask import *
import os, binascii, hashlib
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

app.secret_key = binascii.hexlify(os.urandom(32))

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String, unique=True)
    name = Column(String, unique=True)


engine = create_engine('sqlite:///cms.db', echo=True)
sessdb = sessionmaker(bind=engine)
s = sessdb()


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
    q = s.query(User).filter(User.username == user, User.password == pwd).first()
    if q is None:
        msg = 'Login Failed.'
    else:
        q = s.query(User).filter(User.username == user, User.password == pwd).first()
        session['username'] = q.username
        session['name'] = q.name
        session['logged'] = True
        msg = 'Successful login.'
    return render_template('index.html', msg=msg)


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
    s.add(h)
    s.commit()
    session['username'] = user
    session['logged'] = True
    msg = 'success!'
    return render_template('index.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
