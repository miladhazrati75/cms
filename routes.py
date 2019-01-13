import binascii
import hashlib
import os
from flask_sqlalchemy import SQLAlchemy
from flask import *

app = Flask(__name__)

app.secret_key = binascii.hexlify(os.urandom(32))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cms.db'

db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40), unique=True)
    name = db.Column(db.String(40), unique=True)


class Post(db.Model):
    __tablename__ = 'posts'
    pid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), unique=True)
    body = db.Column(db.String, unique=True)


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
        session['uid'] = qlogin.uid
    return render_template('index.html', msg=session)


@app.route('/Logout')
def logout():
    del session['username']
    del session['logged']
    session['msg'] = 'logged out!'
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
    qedit = User.query.filter(User.username == request.form['user']).first()
    session['username'] = user
    session['logged'] = True
    session['name'] = request.form['name']
    session['msg'] = 'success!'
    session['uid'] = qedit.uid
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

@app.route('/Posts')
def show_posts():
    qpost = Post.query.filter(Post.uid == session['uid']).all()
    title = []
    for i in range(0,5):
        try:
            title.append(qpost[i].title)
        except IndexError:
            continue
    return render_template('posts.html', post=title)


@app.route('/NewPost')
def show_new_post():
    session['form'] = 'post'
    return render_template('posts.html', post=session)


@app.route('/ValidatePost', methods=['GET','POST'])
def new_post():
    post = Post(title=request.form['title'], body=request.form['body'], uid=session['uid'])
    db.session.add(post)
    db.session.commit()
    session['form'] = ''
    session['msg'] = 'Post Created!'
    return redirect('/Posts')


@app.route('/Post/<title>')
def show_post(title):
    qpost = Post.query.filter(Post.uid == session['uid'], Post.title == title).first()
    ptitle = qpost.title
    pbody = qpost.body
    session['post'] = True
    return render_template('showpost.html', content=(ptitle, pbody))


@app.route('/Post/<title>/Delete')
def delete_post(title):
    qpost = Post.query.filter(Post.uid == session['uid'], Post.title == title).first()
    db.session.delete(qpost)
    db.session.commit()
    qpost = Post.query.filter(Post.uid == session['uid']).all()
    title = []
    for i in range(len(qpost)):
        try:
            title.append(qpost[i].title)
        except IndexError:
            continue
    session['msg'] = 'Post Deleted!'
    return render_template('posts.html', post=title)


if __name__ == '__main__':
    app.run(debug=True)
