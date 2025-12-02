#!/usr/bin/python3
"""a class defining a martial arts student"""

import models
from models import storage
from models.base_model import BaseModel, Base
from models.lesson import Lesson
from models.instructor import Instructor
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from os import getenv
import datetime
from utils.security import hash_password


if getenv("MWJ_TYPE_STORAGE") == 'db':
    student_lesson = Table("student_lesson", Base.metadata,
            Column("student_id", String(60), ForeignKey('students.id'), primary_key=True, nullable=False),
            Column("lesson_id", String(60), ForeignKey('lessons.id'), primary_key=True, nullable=False))

    student_instructor = Table("student_instructor", Base.metadata,
            Column("student_id", String(60), ForeignKey("students.id"), primary_key=True, nullable=False),
            Column("instructor_id", String(60), ForeignKey("instructors.id"), primary_key=True, nullable=False))

class Student(BaseModel, Base):
    """a class that iherits from basemodel to define a students attributes"""

    if models.storage_type == "db":
        __tablename__ = "students"
        email = Column(String(60), unique=True, nullable=False)
        password = Column(String(60), nullable=False)
        name = Column(String(60), nullable=False)
        age = Column(Integer, nullable=False)
        lessons = relationship("Lesson", secondary="student_lesson", back_populates="students", cascade="all, delete")
        instructors = relationship("Instructor", secondary="student_instructor", back_populates="students", cascade="all, delete")
        date = Column(DateTime, default=datetime.datetime.utcnow)
    else:
        _instances = []

        email = ""
        password = ""
        name = ""
        age = ""
        lesson_id = ""
        instructor_id = ""
        date = ""
        instructors = []
        lessons = []

    def __init__(self, *args, **kwargs):
        """initialize a stydent"""
        super().__init__(*args, **kwargs)
        if 'email' in kwargs:
            self.email = kwargs['email']
        if 'password' in kwargs:
            self.password = hash_password(kwargs['password'])
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'age' in kwargs:
            self.age = kwargs['age']

        #assign a default instructor if none was explicitly provided
        if models.storage_type == "db" and not getattr(self, "instructors", None):
            default_instructor = None
            for inst in storage.all(Instructor).values():
                if inst.email == "instructor@inst.com":
                    default_instructor = inst
                    break

            #link to default instructor for each student if inst not provided
            if default_instructor:
                self.instructors.append(default_instructor)

    @classmethod
    def all(cls):
        """return all instances of this class"""
        return [str(obj) for key, obj in storage.all().items()
                if key.startswith(cls.__name__ + ".")]

    if models.storage_type != "db":
        @property
        def instructors(self):
            '''return instructors'''
            instructors_values = storage.all(Instructor).values()
            instructors_list = []
            for instructor in instructors_values:
                if instructor.student_id == self.id:
                    instructors_list.append(instructor)
            return instructors_list
