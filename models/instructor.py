#!/usr/bin/python3
"""a class defining a martial arts instructor"""

import models
from models import storage
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Instructor(BaseModel, Base):
    """a class that inherits from basemodel to define an instructors attributes"""

    if models.storage_type == "db":
        __tablename__ = 'instructors'
        email = Column(String(60), nullable=False, unique=True)
        password = Column(String(60), nullable=False)
        name = Column(String(60), nullable=False)
        lessons = relationship("Lesson", secondary="lesson_instructor", back_populates="instructors")
        #lesson_id = Column(String(60), ForeignKey("lessons.id"), nullable=False)
        students = relationship("Student", secondary="student_instructor", back_populates="instructors")
    else:
        _instances = []

        email = ""
        password = ""
        name = ""
        lesson_id = ""

    def __init__(self, *args, **kwargs):
        """initializes instructor"""
        super().__init__(*args, **kwargs)
        if 'email' in kwargs:
            self.email = kwargs['email']
        if 'password' in kwargs:
            self.password = kwargs['password']
        if 'name' in kwargs:
            self.name = kwargs['name']

    @classmethod
    def all(cls):
        """returns all instances of this class"""
        return [str(obj) for key, obj in storage.all().items()
                if key.startswith(cls.__name__ + ".")]

    @classmethod
    def count(cls):
        return len(cls._instances)

