import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://admin:rootroot@db-savood.c0hav88yk9mq.us-east-1.rds.amazonaws.com:3306/foodbank"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class Foodbank(db.Model):
    __tablename__ = 'foodbanks2'

    foodbank_id = db.Column(db.Integer, primary_key=True)
    foodbank_name = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    foodbank_address = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(255), nullable=False)
    region = db.Column(db.Enum('Central', 'North', 'West', 'East', 'North-East'), nullable=False)
    
    def json(self):
        dto = {
            'foodbank_id': self.foodbank_id,
            'foodbank_name': self.foodbank_name,
            'phone_number': self.phone_number,
            'foodbank_address': self.foodbank_address,
            'postal_code': self.postal_code,
            'region': self.region
        }

        return dto

#get foodbank by id
@app.route("/get_foodbank/<foodbank_id>")
def get_foodbank_by_id(foodbank_id):
    pass  #edit ini dong hehe

@app.route("/new_foodbank", methods=['POST'])
def create_foodbank():
    print('hallo')
    data = request.get_json()

    print('ini datanya', data)
    foodbank_id = data.get('foodbank_id')
    foodbank_name = data.get('foodbank_name')
    phone_number = data.get('phone_number')
    foodbank_address = data.get('address')
    postal_code = data.get('postal_code')
    region = data.get('region')

    new_foodbank = Foodbank(foodbank_id = foodbank_id, foodbank_name=foodbank_name, phone_number=phone_number,foodbank_address = foodbank_address, postal_code=postal_code, region=region)

    print(foodbank_id)
    try:
        db.session.add(new_foodbank)
        db.session.commit()
        print('masuk ke data')
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while adding new foodbank" + str(e)
            }
        ), 500
    
    print(json.dumps(new_foodbank.json(), default=str)) # convert a JSON object to a string and print
    print()

    return jsonify(
        {
            "code": 201,
            "data": new_foodbank.json()
        }
    ), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("This is flask for " + os.path.basename(__file__) + ": foodbank")
    app.run(host='0.0.0.0', port=5002, debug=True)