#!/usr/bin/python3
"""
 Test cities access from a state
"""
from models import storage
from models.student import Student
from models.instructor import Instructor

"""
 Objects creations
"""
student_1 = Student(name="California")
print("New student: {}".format(student_1))
student_1.save()
student_2 = Student(name="Arizona")
print("New student: {}".format(student_2))
student_2.save()

instructor_1 = Instructor(student_id=student_1.id, name="Napa")
print("New instructor: {} for the student: {}".format(instructor_1, student_1))
instructor_1.save()
instructor_2 = Instructor(student_id=student_2.id, name="Sonoma")
print("New instructor: {} for the student: {}".format(instructor_2, student_2))
instructor_2.save()
instructor_2_1 = Instructor(student_id=student_2.id, name="Page")
print("New instructor: {} for the student: {}".format(instructor_2_1, student_2))
instructor_2_1.save()


"""
 Verification
"""
print("")
all_students = storage.all(Student)
for student_id, student in all_students.items():
    for instructor in student.instructors:
        print("Find the instructor {} for the student {}".format(instructor, student))

