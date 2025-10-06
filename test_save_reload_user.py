#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel
from models.student import Student
from models.instructor import Instructor

all_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

print("-- Create a new Student --")
my_user = Student()
my_user.first_name = "Betty"
my_user.last_name = "Bar"
my_user.email = "airbnb@mail.com"
my_user.password = "root"
my_user.age = 15
my_user.lesson = "taekwondo"
my_user.save()
print(my_user)

print("-- Create a new Student 2 --")
my_user2 = Student()
my_user2.first_name = "John"
my_user2.email = "airbnb2@mail.com"
my_user2.password = "root"
my_user2.age = 20
my_user2.lesson = "karate"
my_user2.save()
print(my_user2)

print("-- Create a new instructor --")
my_use = Instructor()
my_use.first_name = "John"
my_use.email = "airbnb2@mail.com"
my_use.password = "root"
my_use.last_name = "mwas"
my_use.lesson_instructing = "karate"
my_use.save()
print(my_use)
