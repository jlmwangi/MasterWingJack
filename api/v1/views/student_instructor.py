#!/usr/bin/python3
'''a new view for instructor objects'''

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.instructor import Instructor
from models.student import Student

@app_views.route('/students/<student_id>/instructors', methods=['GET'], strict_slashes=False)
def get_all_instructors_for_student(student_id):
    '''this method gets all instructors associated with a particular student'''
    student = storage.get(Student, student_id)
    if not student:
        abort(404)
    return jsonify({
        "student": student.name,
        "instructors": [ inst.to_dict() for inst in student.instructors]
    })

@app_views.route('/instructors/<instructor_id>/students', methods=['GET'], strict_slashes=False)
def get_all_students_for_instructor(instructor_id):
    '''get all students associated with an instructor'''
    instructor = storage.get(Instructor, instructor_id)
    if not instructor:
        abort(404)

    return jsonify({
        "instructor": instructor.name,
        "students": [student.to_dict() for student in instructor.students]
    })

@app_views.route('/instructors/<instructor_id>/students/<student_id>', methods=['POST'], strict_slashes=False)
def assign_student_to_instructor(instructor_id, student_id):
    '''assigns a student to an instructor'''
    instructor = storage.get(Instructor, instructor_id)
    if not instructor:
        abort(404)

    student = storage.get(Student, student_id)
    if not student:
        abort(404)

    if student in instructor.students:
        return jsonify({"message": "student already assigned"}), 200

    instructor.students.append(student)
    instructor.save()

    return jsonify(instructor.to_dict()), 201

@app_views.route('/instructors/<instructor_id>/students/<student_id>', methods=['DELETE'], strict_slashes=False)
def delete_student_from_instructor(instructor_id, student_id):
    '''deletes a sudent from an instructor'''
    instructor = storage.get(Instructor, instructor_id)
    if not instructor:
        abort(404)

    student = storage.get(Student, student_id)
    if not student:
        abort(404)

    if student in instructor.students:
        instructor.students.remove(student)
        instructor.save()

    return jsonify({}), 200

