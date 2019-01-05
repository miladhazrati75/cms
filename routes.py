from flask import *

app = Flask(__name__)

app.secret_key = 'aweb'


app.route('/')
def home():
    session['username'] = 'admin'
    return render_template('index.html', session=session)


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
