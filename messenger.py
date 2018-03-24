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
@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        message = request.form['message']
        origin = str(request.remote_addr)
    # if request.method == 'GET':
    #    message = request.args.get("message")
    if type(message) !=  type("string"):
        print(type(message))
        message = ""
    else:
        print(message)
        try:
            msg = Messages(message=message, origin=origin)
            db.session.add(msg)
            db.session.commit()
            render_template("index.html", msg=message, is_sent= True if len(message)>0 else False)
        except KeyError:
            db.session.rollback()
            render_template("index.html", msg="", is_sent= False)
        except IntegrityError:
            db.session.rollback()
            render_template("index.html", msg="", is_sent= False)
        except:
            print('General exception')
            
    return render_template("index.html", msg=message, is_sent= True if len(message) > 0 else False)


# Log page
@app.route('/log', methods=['GET', 'POST'])
def log():
    messages = Messages.query.order_by("id desc").all()
    return render_template("log.html", messages=messages)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=5000) #, ssl_context=context)
