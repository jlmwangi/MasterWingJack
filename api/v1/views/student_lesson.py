#!/usr/bin/python3
'''a new view for students and lesson objects'''

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.lesson import Lesson
from models.student import Student

@app_views.route('/students/<student_id>/lessons', methods=['GET'], strict_slashes=False)
def get_all_lessons_for_student(student_id):
    '''this method gets all lessons associated with a particular student'''
    student = storage.get(Student, student_id)
    if not student:
        abort(404)
    return jsonify({
        "student": student.name,
        "lessons": [ lesson.to_dict() for lesson in student.lessons]
    })

@app_views.route('/lessons/<lesson_id>/students', methods=['GET'], strict_slashes=False)
def get_all_students_for_lesson(lesson_id):
    '''get all students associated with a lesson'''
    lesson = storage.get(Lesson, lesson_id)
    if not lesson:
        abort(404)

    return jsonify({
        "lesson": lesson.name,
        "students": [student.to_dict() for student in lesson.students]
    })

@app_views.route('/lessons/<lesson_id>/students/<student_id>', methods=['POST'], strict_slashes=False)
def assign_student_to_lesson(lesson_id, student_id):
    '''assigns a student to an lesson'''
    lesson = storage.get(Lesson, lesson_id)
    if not lesson:
        abort(404)

    student = storage.get(Student, student_id)
    if not student:
        abort(404)

    if student in lesson.students:
        return jsonify({"message": "student already assigned"}), 200

    lesson.students.append(student)
    lesson.save()

    return jsonify(lesson.to_dict()), 201

@app_views.route('/lessons/<lesson_id>/students/<student_id>', methods=['DELETE'], strict_slashes=False)
def delete_student_from_lesson(lesson_id, student_id):
    '''deletes a sudent from a lesson'''
    lesson = storage.get(Lesson, lesson_id)
    if not lesson:
        abort(404)

    student = storage.get(Student, student_id)
    if not student:
        abort(404)

    if student in lesson.students:
        lesson.students.remove(student)
        lesson.save()

    return jsonify({}), 200


