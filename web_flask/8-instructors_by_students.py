#!/usr/bin/python3
'''a script that starts a flask web application'''

from flask import Flask, render_template
import os
from models import storage
from models.student import Student
from models.instructor import Instructor


app = Flask(__name__)



@app.route('/instructors_by_students', strict_slashes=False)
def students_instructors_list():
    '''display a html page containing students and instructors'''
    students = sorted(list(storage.all(Student).values()), key=lambda x : x.name)
    instructors = sorted(list(storage.all(Instructor).values()), key=lambda x : x.name)

    return render_template("8-instructors_by_students.html", students=students, instructors=instructors)


@app.teardown_appcontext
def remove_session(exception):
    '''remove current sqlalchemy session'''
    storage.close()



if __name__ == "__main__":
    host = os.environ.get('HOST', '0.0.0.0')
    port = os.environ.get('PORT', 5000)

    app.run(host=host, port=port, debug=True)
