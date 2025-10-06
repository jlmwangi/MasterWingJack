#!/usr/bin/python3
""" Test delete feature
"""
from models.engine.file_storage import FileStorage
from models.lesson import Lesson

fs = FileStorage()

# All Lessons
all_lessons = fs.all(Lesson)
print("All Lessons: {}".format(len(all_lessons.keys())))
for lesson_key in all_lessons.keys():
    print(all_lessons[lesson_key])

# Create a new Lesson
new_lesson = Lesson()
new_lesson.name = "California"
fs.new(new_lesson)
fs.save()
print("New Lesson: {}".format(new_lesson))

# All States
all_lessons = fs.all(Lesson)
print("All Lessons: {}".format(len(all_lessons.keys())))
for lesson_key in all_lessons.keys():
    print(all_lessons[lesson_key])

# Create another Lesson
another_lesson = Lesson()
another_lesson.name = "Nevada"
fs.new(another_lesson)
fs.save()
print("Another Lesson: {}".format(another_lesson))

# All lessons
all_lessons = fs.all(Lesson)
print("All Lessons: {}".format(len(all_lessons.keys())))
for lesson_key in all_lessons.keys():
    print(all_lessons[lesson_key])        

# Delete the new State
fs.delete(new_lesson)

# All States
all_lessons = fs.all(Lesson)
print("All Lessons: {}".format(len(all_lessons.keys())))
for lesson_key in all_lessons.keys():
    print(all_lessons[lesson_key])
