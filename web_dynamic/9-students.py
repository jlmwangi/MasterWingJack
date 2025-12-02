#!/usr/bin/python3
'''a script that starts a flask web application'''

from flask import Flask, render_template
import os
from models import storage
from models.student import Student
from models.instructor import Instructor
import uuid


app = Flask(__name__)


@app.route('/students', strict_slashes=False)
def students_list():
    '''display a html page containing students'''
    students = sorted(list(storage.all(Student).values()), key=lambda x : x.name)
    cache_id = uuid.uuid4()

    return render_template("7-students_list.html", students=students, cache_id=cache_id)

@app.route('/students/<id>', strict_slashes=False)
def student_instructors_list(id):
    '''display a html page containing students and instructors'''
    students = sorted(list(storage.all(Student).values()), key=lambda x : x.name)
    cache_id = uuid.uuid4()

    student1 = None
    for student in students:
        if student.id == id:
            student1 = student
            break

    """all_instructors = sorted(list(storage.all(Instructor).values()), key=lambda x : x.name)
    instructors = [instructor for instructor in all_instructors if instructor.student_id == id]"""
    instructors = student1.instructors

    return render_template("9-students.html", student=student1, instructors=instructors, cache_id=cache_id)


@app.teardown_appcontext
def remove_session(exception):
    '''remove current sqlalchemy session'''
    storage.close()



if __name__ == "__main__":
    host = os.environ.get('HOST', '0.0.0.0')
    port = os.environ.get('PORT', 5000)

    app.run(host=host, port=port, debug=True)
