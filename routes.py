from flask import *
import os,binascii

app = Flask(__name__)

app.secret_key = binascii.hexlify(os.urandom(32))



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/ValidateLogin',methods=['GET','POST'])
def validatelogin():
    user=request.form['user']
    pwd=request.form['pass']
    session['username']=user
    session['logged']=True
    return render_template('index.html')

@app.route('/Logout')
def logout():
    del session['username']
    del session['logged']
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
