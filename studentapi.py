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
class stundent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    school = db.Column(db.String(200))
    Class = db.Column(db.Float)
    phone = db.Column(db.Integer)

    def __init__(self, name, school, Class, phone):
        self.name = name
        self.school = school
        self.Class = Class
        self.phone = phone

db.create_all()
db.session.commit()

# Product Schema
class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'school', 'Class', 'phone')

#Init Schema
stundent_schema = StudentSchema(strict=True)
stundents_schema = StudentSchema(many=True, strict=True)
# Create a student
@app.route("/add_student", methods=['POST'])
def add_student():
    name = request.form.get("name")
    schoolname = request.form.get("schoolname")
    Class = float(request.form.get("Class"))
    phone = int(request.form.get("phone"))

    new_student = student(name, schoolname, Class, phone)

    db.session.add(new_student)
    db.session.commit()

    return jsonify({"success": True,
                    "name": new_student.name,
                    "schoolname": new_student.schoolname,
                    "Class": new_student.Class,
                    "phone": new_student.phone})

# Get all students
@app.route("/get_student", methods=['GET'])
def get_student():
    all_students = student.query.all()
    result = students_schema.dump(all_students)
    return jsonify(result.data)

# Get single student
@app.route("/one_student", methods=['GET','POST'])
def one_student():
    number = request.form.get("number")
    singlestudent = student.query.get(number)
    return jsonify({"success": True,
                    "id": singlestudent.id,
                    "name": singlestudent.name,
                    "Class": singlestudent.Class,
                    "phone": singlestudent.phone})


# Update a student
@app.route("/update_student", methods=['PUT'])
def update_student():

    id = request.form.get('number');
    singlestudent = student.query.get(id)

    name = request.form.get("name")
    schoolname = request.form.get("schoolname")
    Class = float(request.form.get("Class"))
    phone = int(request.form.get("phone"))


    singlestudent.name = name
    singlestudent.schoolname = schoolname
    singlestudent.Class = Class
    singlestudent.phone = phone

    db.session.commit()

    return jsonify({"success": True,
                    "id": singlestudent.id,
                    "name": singlestudent.name,
                    "Class": singlestudent.Class,
                    "phone": singlestudent.phone})


# Delete a student
@app.route("/delete_student", methods=['DELETE'])
def delete_student():

    number = request.form.get("number")
    singlestudent = student.query.get(number)

    id = singlestudent.id,
    name = singlestudent.name,
    schoolname = singlestudent.schoolname,
    Class = singlestudent.Class,
    phone = singlestudent.phone

    db.session.delete(singlestudent)
    db.session.commit()

    return jsonify({"success": True,
                    "id": id,
                    "name": name,
                    "schoolname": schoolname,
                    "Class": Class,
                    "phone": phone})

# Run Server
if __name__=='__main__':
    app.run(debug=True)
