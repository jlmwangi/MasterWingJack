#!/usr/bin/python3
"""a class defining a martial arts student"""

import models
from models import storage
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv


if getenv("MWJ_TYPE_STORAGE") == 'db':
    lesson_instructor = Table("lesson_instructor", Base.metadata,
        Column("lesson_id", String(60), ForeignKey("lessons.id"), primary_key=True),
        Column("instructor_id", String(60), ForeignKey("instructors.id"), primary_key=True))

class Lesson(BaseModel, Base):
    """a class that iherits from basemodel to define a students attributes"""

    if models.storage_type == 'db':
        __tablename__ = "lessons"
        name = Column(String(60), nullable=False, unique=True)
        duration = Column(Integer, nullable=False)
        #instructor_id = Column(String(60), ForeignKey("instructors.id"), unique=True)
        instructors = relationship("Instructor", secondary="lesson_instructor", back_populates="lessons")
        students = relationship("Student", secondary="student_lesson", back_populates="lessons")
    else:
        name = ""
        duration = ""
        instructor_id = ""
        instructors = []
        students = []

    def __init__(self, *args, **kwargs):
        """initializes the lesson"""
        super().__init__(*args, **kwargs)
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'duration' in kwargs:
            self.duration = kwargs['duration']

    @classmethod
    def all(cls):
        """return all instances of this class"""
        return [obj for key, obj in storage.all().items()
                if key.startswith(cls.__name__ +".")]

    if getenv("MWJ_TYPE_STORAGE") != "db":
        @property
        def instructors(self):
            """returns list of instructors associated with the lesson"""
            instructors_values = storage.all(Instructor).values()
            instructors_list = []
            for instructor in instructors_values:
                if instructor.lesson_id == self.id:
                    instructors_list.append(instructor)
            return instructors_list
