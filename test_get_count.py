#!/usr/bin/python3
""" Test .get() and .count() methods
"""

from models import storage
from models.student import Student

print("All objects: {}".format(storage.count()))
print("Student objects: {}".format(storage.count(Student)))

first_student_id = list(storage.all(Student).values())[0].id
print("First student: {}".format(storage.get(Student, first_student_id)))
