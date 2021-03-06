"""
This program was written by Máté Szedlák (C) 2018 (szedlakmate@gmail.com). All rights reserved.

Source:
https://github.com/szedlakmate/led-clock-messenger/
"""


import os
import threading
import datetime
import time
import random
import string
from flask import Flask, url_for, redirect, render_template, session, request
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy


# Initialize web app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://messenger:demopassword@localhost/messenger'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suggested by SQLAlchemy
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10)) #'pSJz+u)zq*.9VN~t'
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


# Messages types model
class Commands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String(80), unique=False, nullable=False)
    shown = db.Column(db.Boolean, unique=False, nullable=False, default = False)
    sent = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.datetime.utcnow)
    origin =db.Column(db.String(20), nullable=True)

    def __init__(self, command, origin):
        self.command = command
        self.shown = False
        # self.sent = datetime.datetime.utcnow
        if (origin):
            self.origin = origin

    def __repr__(self):
        return self.command


try:
    db.create_all()
except IntegrityError:
    db.session.rollback()


def schedule_command(command, origin):
    try:
        cmd = Commands(command=command, origin=origin)
        db.session.add(cmd)
        db.session.commit()
    except KeyError:
        db.session.rollback()
    except IntegrityError:
        db.session.rollback()
    except:
        print('General exception')


# Landing page
@app.route('/', methods=['GET'])
def index():
    is_sent = False
    message = session.get('message')
    session.clear()
    if type(message) != type("string"):
        message = ""
    else:
        is_sent = True
    return render_template("index.html", msg=message, is_sent=is_sent)


# Landing page - POST message
@app.route('/', methods=['POST'])
def index_POST():
    message = request.form['message']
    origin = str(request.remote_addr)
    if type(message) != type("string"):
        print(type(message))
    else:
        print(message + ' (' + origin + ')')
        try:
            msg = Messages(message=message, origin=origin)
            db.session.add(msg)
            db.session.commit()
            session.clear()
            session['message'] = message
            return redirect(url_for('index'))
        except KeyError:
            db.session.rollback()
            render_template("index.html", msg="", is_sent=False)
        except IntegrityError:
            db.session.rollback()
            render_template("index.html", msg="", is_sent=False)
        except:
            print('General exception')

    return render_template("index.html", msg="", is_sent=False)


# Log page
@app.route('/log')
def log():
    messages = Messages.query.order_by("id desc").all()
    return render_template("log.html", messages=messages)


# Control panel page
@app.route('/manage', methods=['GET'])
def manage():
    action = session.get('action')
    note = session.get('note')
    origin = str(request.remote_addr)
    session.clear()
    if type(action) != type("string"):
        action = ""
    if type(note) != type("string"):
        note = ""
    if type(origin) != type("string"):
        origin = ""

    if action == "r-clock":
        t = threading.Thread(
            target=schedule_command(
                "sudo -H python3 /home/pi/Projects/led-clock-messenger/restart.py", origin))
        t.start()
    elif action == "r-pi":
        t = threading.Thread(
            target=schedule_command(
                "sudo reboot", origin))
        t.start()
    elif action == "s-pi":
        t = threading.Thread(
            target=schedule_command(
                "sudo shutdown", origin))
        t.start()
    return render_template("manage.html", action=note)


# Landing page - POST message
@app.route('/manage', methods=['POST'])
def manage_POST():
    action = request.form['action']
    origin = str(request.remote_addr)
    if type(action) != type("string"):
        print(type(action))
    else:
        print(action + ' (' + origin + ')')
        try:
            if action == 'R-clock':
                session.clear()
                session['action'] = "r-clock"
                session['note'] = 'Clock and Messenger have been restarted'
                return redirect(url_for('manage'))
            elif action == 'R-pi':
                session.clear()
                session['action'] = "r-pi"
                session['note'] = 'Raspberry has been restarted'
                return redirect(url_for('manage'))
            elif action == 'S-pi':
                session.clear()
                session['action'] = "s-pi"
                session['note'] = 'Raspberry has been shut down'
                return redirect(url_for('manage'))
        except:
            print('General exception')

    return render_template("manage.html", action="")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5000) #, ssl_context=context)
