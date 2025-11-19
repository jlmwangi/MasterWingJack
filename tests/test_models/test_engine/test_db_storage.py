#!/usr/bin/python3
"""test file storage"""

import os

os.environ["MWJ_TYPE_STORAGE"] = "db"
os.environ["MWJ_ENV"] = "test"



import unittest
from models import storage
from models.base_model import BaseModel
from models.student import Student
from models.engine.db_storage import DBStorage
import json
from sqlalchemy.exc import IntegrityError



class TestDbStorage(unittest.TestCase):
    """test DBStorage class"""
    def setUp(self):
        '''initialize db storage'''
        """import os

        os.environ["MWJ_TYPE_STORAGE"] = "db"
        os.environ["MWJ_ENV"] = "test"
        """

        self.storage = DBStorage()
        self.storage.reload()

        student = Student(
                name="Mary",
                email="m@g.com",
                password="pwd",
                age=30
                )
        self.storage.new(student)
        self.storage.save()
        self.student_id = student.id

    def tearDown(self):
        self.storage.close()

    def test_all_students(self):
        '''test method all'''
        result = self.storage.all(Student)
        key = f"Student.{self.student_id}"
        self.assertIn(key, result)

    def test_all_returns_all_objs(self):
        """test that the all method when passed none returns all objects"""
        result = self.storage.all()
        key = f"Student.{self.student_id}"
        self.assertIn(key, result)

    def test_all_takes_only_objs_of_type_obj(self):
        """test that all this method takes is object of type obj"""
        classnames = {
                "student": Student
                }
        cls = None
        for k, v in classnames.items():
            cls = v

        res = self.storage.all(Student)
        for key, val in res.items():
            obj = val
            self.assertIsInstance(obj, cls)

    def test_raises_integrity_error_without_certain_values(self):
        """test that calling student with some nullable values raises errors"""
        with self.assertRaises(IntegrityError):
            student1 = Student(name="jb")
            self.storage.new(student1)
            """self.storage.save()
            result = self.storage.all(Student)
            key = f"Student.{student1.id}"
            self.assertIn(key, result)"""

    def test_new_adds_obj(self):
        """test that adding a new object persists it"""
        student2 = Student(
                name="name",
                email="email",
                password="passw",
                age=20
                )
        self.storage.new(student2)

        key = f"Student.{student2.id}"
        result = self.storage.all()

        self.assertIn(key, result)

    def test_new_takes_arg(self):
        """test that new method raises an error when not called with an object argument"""
        with self.assertRaises(TypeError):
            self.storage.new()

    def test_delete_method(self):
        """test delete removes obj from storage"""
        student3 = Student(
                name="who",
                email="when@g.com",
                password="what",
                age=13
            )
        self.storage.new(student3)
        result = self.storage.all(Student)
        key = f"Student.{student3.id}"
        self.assertIn(key, result)

        self.storage.delete(student3)
        result1 = self.storage.all()
        self.assertNotIn(key, result1)

    def test_delete_only_works_with_arg(self):
        """test that the delete method only works when an argument is passed or returns none when no arg is passed"""
        key = f"Student.{self.student_id}"
        result = self.storage.all()
        self.storage.delete()

        self.assertIn(key, result)

        student = None
        for k, obj in result.items():
            if k == key:
                student = obj

        self.storage.delete(student)
        res = self.storage.all(Student)

        self.assertNotIn(key, res)

    def test_get_method(self):
        """test get method retrieves one object based on cls and id"""
        #student_id = f"{student.id}"
        key = f"Student.{self.student_id}"
        result = self.storage.get(Student, self.student_id)

        self.assertIsInstance(result, Student)
        self.assertIn(key, self.storage.all())
        self.assertEqual(result.id, self.student_id)

    def test_count_method(self):
        '''test that count method counts number of objects in storage'''
        result = self.storage.count(Student)
        res = self.storage.count()

        self.assertEqual(result, res)
        student3 = Student(
                name="who",
                email="when@g.com",
                password="what",
                age=13
            )
        self.storage.new(student3)

        res2 = self.storage.count(Student)
        self.assertGreater(res2, res)

