from os import name
from re import I
from flask import Flask,render_template,request,session,jsonify
import flask
from flask_sqlalchemy import SQLAlchemy
from collections import namedtuple
import json
application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:password123@database-1.cb1v5s5uduqk.us-east-2.rds.amazonaws.com:3306/pyposdb"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(application)

ItemData = namedtuple("ItemData",['itemId','itemDesc','itemPrice','itemQty'])

import model.Item as Item

db.create_all()
db.session.commit()

@application.route('/')
def route_home():
    return render_template('index.html')

@application.route('/item',methods=['GET','POST','PUT','DELETE'])
def route_item():
    if request.method == 'GET':
        itm = db.session.query(Item.Item).all()
        return render_template('item.html',itms=itm)
        # return jsonify({'data':itm})
    elif request.method == 'POST':
       data = request.get_json()
       data = ItemData(**data)
       if data.itemId != None and data.itemDesc != None and data.itemPrice != None and data.itemQty != None :
           itm = Item.Item(data.itemId,data.itemDesc,data.itemPrice,data.itemQty)
           db.session.add(itm)
           db.session.commit()
           return jsonify({'status':'Success'})
    elif request.method == 'PUT':
        itemId = request.args.get('itemId')
        data = request.get_json()
        data = ItemData(**data)
        db.session.query(Item.Item).filter_by(id=itemId).update(dict(description=data.itemDesc,unit_price=data.itemPrice,qty=data.itemQty))
        db.session.commit()
        return jsonify({'status':'Success'})
    elif request.method == 'DELETE':
        itemId = request.args.get('itemId')
        db.session.query(Item.Item).filter(Item.Item.id == itemId).delete()
        db.session.commit()
        db.session.flush()
        return jsonify({ 'status':'Success' })

@application.errorhandler(404)
def error_404(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    application.run(debug=True)