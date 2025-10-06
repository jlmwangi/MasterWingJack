#!/usr/bin/python3
""" Test link Many-To-Many Place <> Amenity
"""
from models.student import Student
from models.lesson import Lesson
from models.instructor import Instructor
import models
from models import storage

# creation of a Student
student = Student(name="Cafornia", email="email@eil.com", password="pass", age=20)
student.save()

# creation of 2 Lessons
lesson_1 = Lesson(duration=140, name="House 1")
lesson_1.save()
lesson_2 = Lesson(duration=60, name="House 2")
lesson_2.save()

# creation of 3 various instructors
instructor_1 = Instructor(email="mm@g.com", password="passwo", name="Wifi")
instructor_1.save()
instructor_2 = Instructor(email="hh@f.com", password="passwo", name="Cable")
instructor_2.save()
instructor_3 = Instructor(email="gg@gm.com", password="pass", name="Oven")
instructor_3.save()

# link place_1 with 2 amenities
lesson_1.instructors.append(instructor_1)
lesson_1.instructors.append(instructor_2)

# link place_2 with 3 amenities
lesson_2.instructors.append(instructor_1)
lesson_2.instructors.append(instructor_2)
lesson_2.instructors.append(instructor_3)

storage.save()

print("OK")
