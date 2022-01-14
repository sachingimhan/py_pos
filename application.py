from flask import Flask, render_template, request, session, jsonify
import flask
from flask_sqlalchemy import SQLAlchemy
from collections import namedtuple
import json
# Config
application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:password123@database-1.cb1v5s5uduqk.us-east-2.rds.amazonaws.com:3306/pyposdb"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(application)
# Touples
ItemData = namedtuple(
    "ItemData", ['itemId', 'itemDesc', 'itemPrice', 'itemQty'])
UserData = namedtuple("UserData", ['email', 'password'])

import model.Item as Item
from model.User import User


db.create_all()
db.session.commit()


@application.route('/')
def route_home():
    return render_template('login.html')

@application.route('/dash',methods=['GET'])
def route_dash():
    return render_template('index.html')

@application.route('/reg',methods=['POST','GET'])
def route_reg():
    if request.method == 'POST':
        try:
            data = request.get_json()
            data = UserData(**data)
            user = User(data.email,data.password)
            db.session.add(user)
            db.session.commit()
            return jsonify({'status': 'Success', 'data': user}), 200
        except Exception as e:
            return jsonify({'status': 'Can not create user', 'data': e.__cause__}), 400
    elif request.method == 'GET':
        return render_template('reg.html')

@application.route('/login',methods=['POST','GET'])
def route_login():
    if request.method == 'POST':
        try:
            data = request.get_json()
            data = UserData(**data)
            user = User.query.filter(User.email == data.email,User.password == data.password).one()
            return jsonify({'status': 'Success', 'data': True}), 200
        except Exception as e:
            return jsonify({'status': 'User Not Found', 'data': e.__cause__}), 400
    elif request.method == 'GET':
        return render_template('login.html')

@application.route('/item/<id>', methods=['GET'])
def route_item_search(id):
    try:
        if request.method == 'GET':
            search = db.session.query(Item.Item).filter_by(id=id).one()
            return jsonify({'status': 'Success', 'data': search}), 200
    except Exception as e:
        return jsonify({'status': 'Fail','data':e.__cause__}), 400


@application.route('/item', methods=['GET', 'POST', 'PUT', 'DELETE'])
def route_item():
    try:
        if request.method == 'GET':
            itm = db.session.query(Item.Item).all()
            return render_template('item.html', itms=itm)
        elif request.method == 'POST':
            data = request.get_json()
            data = ItemData(**data)
            if data.itemId != None and data.itemDesc != None and data.itemPrice != None and data.itemQty != None:
                itm = Item.Item(data.itemId, data.itemDesc,
                            data.itemPrice, data.itemQty)
                db.session.add(itm)
                db.session.commit()
                return jsonify({'status': 'Success'})
            else:
                return jsonify({'status': 'Fail'})
        elif request.method == 'PUT':
            itemId = request.args.get('itemId')
            data = request.get_json()
            data = ItemData(**data)
            db.session.query(Item.Item).filter_by(id=itemId).update(
                            dict(description=data.itemDesc, unit_price=data.itemPrice, qty=data.itemQty))
            db.session.commit()
            return jsonify({'status': 'Success'})
        elif request.method == 'DELETE':
            itemId = request.args.get('itemId')
            db.session.query(Item.Item).filter(Item.Item.id == itemId).delete()
            db.session.commit()
            db.session.flush()
            return jsonify({'status': 'Success'})
    except Exception as e:
        return jsonify({'status': 'Fail','data':e.__cause__}), 400
    


@application.errorhandler(404)
def error_404(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    application.run(debug=True)
