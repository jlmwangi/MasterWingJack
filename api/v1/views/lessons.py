#!/usr/bin/python3
'''a new view for student objects'''

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.lesson import Lesson

@app_views.route('/lessons', methods=['GET'], strict_slashes=False)
def get_lessons():
    '''retrieves list of all lessons'''
    lessons_list = []
    for lesson in storage.all(Lesson).values():
        lessons_list.append(lesson.to_dict())

    return jsonify(lessons_list)

@app_views.route('/lessons/<lesson_id>', methods=['GET'], strict_slashes=False)
def get_lesson(lesson_id):
    '''retrieve a single lesson'''
    lesson = storage.get(Lesson, lesson_id)
    if not lesson:
        abort(404)

    return jsonify(lesson.to_dict())

@app_views.route('/lessons/<lesson_id>', methods=['DELETE'], strict_slashes=False)
def delete_lesson(lesson_id):
    '''delete a lesson'''
    lesson = storage.get(Lesson, lesson_id)
    if not lesson:
        abort(404)
    else:
        storage.delete(lesson)
        return jsonify({}), 200

@app_views.route('/lessons', methods=['POST'], strict_slashes=False)
def create_lesson():
    '''create a lesson'''
    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    name = data.get("name")
    duration = data.get("duration")

    if not name:
        return jsonify({"error": "Missing Name"}), 400
    if not duration:
        return jsonify({"error": "Missing Duration"}), 400

    lesson = Lesson(name=name, duration=duration)
    lesson.save()

    return jsonify(lesson.to_dict()), 201

@app_views.route('/lessons/<lesson_id>', methods=['PUT'], strict_slashes=False)
def update_lesson(lesson_id):
    '''updates a lesson based on id'''
    lesson = storage.get(Lesson, lesson_id)
    if not lesson:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignore = ["id", "created_at", "updated_at"]

    for key, value in data.items():
        if key not in ignore:
            setattr(lesson, key, value)

    lesson.save()
    return jsonify(lesson.to_dict()), 200
