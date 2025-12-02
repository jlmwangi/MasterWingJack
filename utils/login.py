#!/usr/bin/python3
'''check password and login user'''

from utils.security import check_password
from models.student import Student
from models.instructor import Instructor
from flask import session


def login_user(email, password):
    '''login user based on email and password'''
    user = Student.query.filter_by(email=email).first()
    if not user:
        user = Instructor.query.filter_by(email=email).first()

    if not user:
        return None  #user not found

    if check_password(password, user.password):
        return user  #login success

    return None  #invalid credentials

