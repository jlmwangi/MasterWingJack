#!/usr/bin/python3
'''a new view for instructors and lesson objects'''

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.instructor import Instructor
from models.lesson import Lesson

@app_views.route('/instructor/<instructor_id>/lessons', methods=['GET'], strict_slashes=False)
def get_all_lessons_for_instructor(instructor_id):
    '''this method gets all lessons associated with a particular instructor'''
    instructor = storage.get(Instructor, instructor_id)
    if not instructor:
        abort(404)
    return jsonify({
        "instructor": instructor.name,
        "lessons": [ lesson.to_dict() for lesson in instructor.lessons]
    })

@app_views.route('/lessons/<lesson_id>/instructors', methods=['GET'], strict_slashes=False)
def get_all_instructors_for_lesson(lesson_id):
    '''get all instructors associated with a lesson'''
    lesson = storage.get(Lesson, lesson_id)
    if not lesson:
        abort(404)

    return jsonify({
        "lesson": lesson.name,
        "instructors": [instructor.to_dict() for instructor in lesson.instructors]
    })

@app_views_route('/lessons/<lesson_id>/instructors/<instructor_id>', methods=['POST'], strict_slashes=False)
def assign_instructor_to_lesson(lesson_id, instructor_id):
    '''assigns an instructor to a lesson'''
    lesson = storage.get(Lesson, lesson_id)
    if not lesson:
        abort(404)

    instructor = storage.get(Instructor, instructor_id)
    if not instructor:
        abort(404)

    if instructor in lesson.instructors:
        return jsonify({"message": "instructor already assigned"}), 200

    lesson.instructors.append(instructor)
    lesson.save()

    return jsonify(lesson.to_dict()), 201

@app_views.route('/lessons/<lesson_id>/instructors/<instructor_id>', methods=['DELETE'], strict_slashes=False)
def delete_instructor_from_lesson(lesson_id, instructor_id):
    '''deletes instructor from a lesson'''
    lesson = storage.get(Lesson, lesson_id)
    if not lesson:
        abort(404)

    instructor = storage.get(Instructor, instructor_id)
    if not instructor:
        abort(404)

    if instructor in lesson.instructors:
        lesson.instructors.remove(instructor)
        lesson.save()

    return jsonify({}), 200
