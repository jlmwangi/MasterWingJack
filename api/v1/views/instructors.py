#!/usr/bin/python3
'''a new view for instructor objects'''

from flask import jsonify, abort, request, render_template
from api.v1.views import app_views
from models import storage
from models.instructor import Instructor
import uuid


@app_views.route('/instructors', methods=['GET'], strict_slashes=False)
def get_instructors():
    '''retrieves list of all instructors'''
    instructors_list = []
    cache_id = uuid.uuid4()

    for instructor in storage.all(Instructor).values():
        instructors_list.append(instructor.to_dict())

    return jsonify(instructors_list)
    #return render_template("instructors.html", instructors=instructors_list, cache_id=cache_id)

@app_views.route('/instructors/<instructor_id>', methods=['GET'], strict_slashes=False)
def get_instructor(instructor_id):
    '''retrieve a single instructor'''
    instructor = storage.get(Instructor, instructor_id)
    if not instructor:
        abort(404)

    return jsonify(instructor.to_dict())

@app_views.route('/instructors/<instructor_id>', methods=['DELETE'], strict_slashes=False)
def delete_instructor(instructor_id):
    '''delete an instructor'''
    instructor = storage.get(Instructor, instructor_id)
    if not instructor:
        abort(404)
    else:
        storage.delete(instructor)
        return jsonify({}), 200

@app_views.route('/instructors', methods=['POST'], strict_slashes=False)
def create_instructor():
    '''create instructor'''
    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name:
        return jsonify({"error": "Missing Name"}), 400
    if not email:
        return jsonify({"error": "Missing Email"}), 400
    if not password:
        return jsonify({"error": "Missing Password"}), 400

    instructor = Instructor(name=name, email=email, password=password)
    instructor.save()

    return jsonify(instructor.to_dict()), 201

@app_views.route('/instructors/<instructor_id>', methods=['PUT'], strict_slashes=False)
def update_instructor(instructor_id):
    '''updates instructor based on id'''
    instructor = storage.get(Instructor, instructor_id)
    if not instructor:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignore = ["id", "created_at", "updated_at"]

    for key, value in data.items():
        if key not in ignore:
            setattr(instructor, key, value)

    instructor.save()
    return jsonify(instructor.to_dict()), 200
