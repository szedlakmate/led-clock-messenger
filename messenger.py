"""
This program was written by Máté Szedlák (C) 2018 (szedlakmate@gmail.com). All rights reserved.

Source:
https://github.com/szedlakmate/led-clock-messenger/
"""

import datetime
from flask import Flask, url_for, redirect, render_template, jsonify, session, request
from sqlalchemy.exc import IntegrityError, OperationalError
from flask_sqlalchemy import SQLAlchemy


# Initialize web app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/messenger'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suggested by SQLAlchemy
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'pSJz+u)zq*.9VN~t'
db = SQLAlchemy(app)


# Messages types model
class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(80), unique=False, nullable=False)
    shown = db.Column(db.Boolean, unique=False, nullable=False, default = False)
    sent = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.datetime.utcnow)
    origin =db.Column(db.String(20), nullable=True)

    def __init__(self, message, origin):
        self.message = message
        self.shown = False
        # self.sent = datetime.datetime.utcnow
        if (origin):
            self.origin = origin

    def __repr__(self):
        return self.message


try:
    db.create_all()
except IntegrityError:
    db.session.rollback()


# Landing page
@app.route('/', methods=['GET'])
def index():
    print('GET')
    is_sent = False
    message = session.get('message')
    session.clear()
    if type(message) != type("string"):
        message = ""
    else:
        is_sent = True
    return render_template("index.html", msg=message, is_sent=is_sent)


# Landing page
@app.route('/', methods=['POST'])
def index_POST():
    print('POST')
    message = request.form['message']
    origin = str(request.remote_addr)
    if type(message) != type("string"):
        print(type(message))
        message = ""
    else:
        print(message + ' (' + origin + ')')
        try:
            msg = Messages(message=message, origin=origin)
            db.session.add(msg)
            db.session.commit()
            session.clear()
            session['message'] = message
            return redirect(url_for('index'))
            #render_template("index.html", msg=message, is_sent=True if len(message)>0 else False)
        except KeyError:
            db.session.rollback()
            render_template("index.html", msg="", is_sent=False)
        except IntegrityError:
            db.session.rollback()
            render_template("index.html", msg="", is_sent=False)
        #except:
        #    print('General exception')

    return render_template("index.html", msg="", is_sent=False)


# Log page
@app.route('/log')
def log():
    messages = Messages.query.order_by("id desc").all()
    return render_template("log.html", messages=messages)

# Control panel page
@app.route('/manage', methods=['GET', 'POST'])
def manage():
    action = ""
    if request.method == 'POST':
        sender_timestamp = request.form['timestamp']
        origin = str(request.remote_addr)
    # if request.method == 'GET':
    #    message = request.args.get("message")
    if type(action) !=  type("string"):
        print(type(action))
    #else:
    return render_template("manage.html", action=action)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5000) #, ssl_context=context)
