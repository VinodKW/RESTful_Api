import os
from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Init app
app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)

# Products class
class product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

db.create_all()
db.session.commit()

# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')

#Init Schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)

# ----------------------------------------- HTML CONTENT----------------------------------------------#

# Index Page
@app.route("/")
def index():
    return render_template("index.html")


# Create Page
@app.route("/create")
def create():
    return render_template("create.html")

# Read Page
@app.route("/read")
def read():
    return render_template("read.html")

# Update Page
@app.route("/update")
def update():
    return render_template("update.html")

# Delete Page
@app.route("/delete")
def delete():
    return render_template("delete.html")

# ----------------------------------------- API CONTENT--------------------------------------------#


# Create a Product
@app.route("/add_product", methods=['POST'])
def add_product():
    name = request.form.get("name")
    description = request.form.get("description")
    price = float(request.form.get("price"))
    qty = int(request.form.get("qty"))

    new_product = product(name, description, price, qty)

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"success": True,
                    "name": new_product.name,
                    "description": new_product.description,
                    "price": new_product.price,
                    "qty": new_product.qty})

# Get all products
@app.route("/get_product", methods=['GET'])
def get_product():
    all_products = product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result.data)

# Get single product
@app.route("/one_product", methods=['GET','POST'])
def one_product():
    number = request.form.get("number")
    singleproduct = product.query.get(number)
    return jsonify({"success": True,
                    "id": singleproduct.id,
                    "name": singleproduct.name,
                    "price": singleproduct.price,
                    "qty": singleproduct.qty})


# Update a product
@app.route("/update_product", methods=['PUT'])
def update_product():

    id = request.form.get('number');
    singleproduct = product.query.get(id)

    name = request.form.get("name")
    description = request.form.get("description")
    price = float(request.form.get("price"))
    qty = int(request.form.get("qty"))


    singleproduct.name = name
    singleproduct.description = description
    singleproduct.price = price
    singleproduct.qty = qty

    db.session.commit()

    return jsonify({"success": True,
                    "id": singleproduct.id,
                    "name": singleproduct.name,
                    "price": singleproduct.price,
                    "qty": singleproduct.qty})


# Delete a product
@app.route("/delete_product", methods=['DELETE'])
def delete_product():

    number = request.form.get("number")
    singleproduct = product.query.get(number)

    id = singleproduct.id,
    name = singleproduct.name,
    description = singleproduct.name,
    price = singleproduct.price,
    qty = singleproduct.qty

    db.session.delete(singleproduct)
    db.session.commit()

    return jsonify({"success": True,
                    "id": id,
                    "name": name,
                    "description": description,
                    "price": price,
                    "qty": qty})

# Run Server
if __name__=='__main__':
    app.run(debug=True)
