#!/usr/bin/python3
'''a new view for student objects'''

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.student import Student

@app_views.route('/students', methods=['GET'], strict_slashes=False)
def get_students():
    '''retrieves list of all students'''
    students_list = []
    for student in storage.all(Student).values():
        students_list.append(student.to_dict())

    return jsonify(students_list)

@app_views.route('/students/<student_id>', methods=['GET'], strict_slashes=False)
def get_student(student_id):
    '''retrieve a single student'''
    student = storage.get(Student, student_id)
    if not student:
        abort(404)

    return jsonify(student.to_dict())

@app_views.route('/students/<student_id>', methods=['DELETE'], strict_slashes=False)
def delete_student(student_id):
    '''delete a student'''
    student = storage.get(Student, student_id)
    if not student:
        abort(404)
    else:
        storage.delete(student)
        return jsonify({}), 200

@app_views.route('/students', methods=['POST'], strict_slashes=False)
def create_student():
    '''create a student'''
    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    age = data.get("age")

    if not name:
        return jsonify({"error": "Missing Name"}), 400
    if not email:
        return jsonify({"error": "Missing Email"}), 400
    if not password:
        return jsonify({"error": "Missing Password"}), 400
    if age is None:
        return jsonify({"error": "Missing Age"}), 400

    student = Student(name=name, email=email, password=password, age=age)
    student.save()

    return jsonify(student.to_dict()), 201

@app_views.route('/students/<student_id>', methods=['PUT'], strict_slashes=False)
def update_student(student_id):
    '''updates a student based on id'''
    student = storage.get(Student, student_id)
    if not student:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignore = ["id", "created_at", "updated_at"]

    for key, value in data.items():
        if key not in ignore:
            setattr(student, key, value)

    student.save()
    return jsonify(student.to_dict()), 200
