import os
from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Init app
app = Flask(__dish__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)

# Products class
class dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, dish, description, price, qty):
        self.dish = dish
        self.description = description
        self.price = price
        self.qty = qty

db.create_all()
db.session.commit()

# Product Schema
class DishSchema(ma.Schema):
    class Meta:
        fields = ('id', 'dish', 'description', 'price', 'qty')

#Init Schema
dish_schema = DishSchema(strict=True)
dishs_schema = DishSchema(many=True, strict=True)
# Create a dish
@app.route("/add_dish", methods=['POST'])
def add_dish():
    dish = request.form.get("dish")
    description = request.form.get("description")
    price = float(request.form.get("price"))
    qty = int(request.form.get("qty"))

    new_dish = dish(dish, description, price, qty)

    db.session.add(new_dish)
    db.session.commit()

    return jsonify({"success": True,
                    "dish": new_dish.dish,
                    "description": new_dish.description,
                    "price": new_dish.price,
                    "qty": new_dish.qty})

# Get all dishs
@app.route("/get_dish", methods=['GET'])
def get_dish():
    all_dishs = dish.query.all()
    result = dishs_schema.dump(all_dishs)
    return jsonify(result.data)

# Get single dish
@app.route("/one_dish", methods=['GET','POST'])
def one_dish():
    number = request.form.get("number")
    singledish = dish.query.get(number)
    return jsonify({"success": True,
                    "id": singledish.id,
                    "dish": singledish.dish,
                    "price": singledish.price,
                    "qty": singledish.qty})


# Update a dish
@app.route("/update_dish", methods=['PUT'])
def update_dish():

    id = request.form.get('number');
    singledish = dish.query.get(id)

    dish = request.form.get("dish")
    description = request.form.get("description")
    price = float(request.form.get("price"))
    qty = int(request.form.get("qty"))


    singledish.dish = dish
    singledish.description = description
    singledish.price = price
    singledish.qty = qty

    db.session.commit()

    return jsonify({"success": True,
                    "id": singledish.id,
                    "dish": singledish.dish,
                    "price": singledish.price,
                    "qty": singledish.qty})


# Delete a dish
@app.route("/delete_dish", methods=['DELETE'])
def delete_dish():

    number = request.form.get("number")
    singledish = dish.query.get(number)

    id = singledish.id,
    dish = singledish.dish,
    description = singledish.description,
    price = singledish.price,
    qty = singledish.qty

    db.session.delete(singledish)
    db.session.commit()

    return jsonify({"success": True,
                    "id": id,
                    "dish": dish,
                    "description": description,
                    "price": price,
                    "qty": qty})

# Run Server
if __dish__=='__main__':
    app.run(debug=True)
