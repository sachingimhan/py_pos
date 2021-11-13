from os import name
from re import S
from flask import Flask,render_template,request
import flask
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:admin1234@aa155qin9bd71l6.cb1v5s5uduqk.us-east-2.rds.amazonaws.com:3306/ebdb"
db = SQLAlchemy(application)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

db.create_all()

@application.route('/')
def route_home():
    return render_template('index.html')

@application.route('/item')
def route_item():
    return render_template('item.html')

@application.route("/items")
def add_item():
    user = User(username='admin', email='admin@example.com')
    db.session.add(user)
    db.session.commit()
    return "Item Added"

if __name__ == '__main__':
    application.run(debug=True)