#!/usr/bin/python3
"""test file storage"""

import os

'''os.environ["MWJ_TYPE_STORAGE"] = "file"
os.environ["MWJ_ENV"] = "test"'''

import unittest
from models import storage
from models.base_model import BaseModel
import json


class TestFileStorage(unittest.TestCase):
    """Test class File Storage"""
    def setUp(self):
        self.test_file = "test_file.json"
        self.objects = {}        

        storage._FileStorage__file_path = self.test_file
        storage._FileStorage__objects = self.objects
        storage._FileStorage__objects.clear()

    def tearDown(self):
        '''clean up test file after each test'''
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_all_method(self):
        """test that all method returns a dictionary"""
        obj = storage.all()

        self.assertIsInstance(obj, dict)

    def test_new_adds_object(self):
        """test it sets obj in objects"""
        obj = BaseModel()
        storage.new(obj)
        storage.save()

        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key], obj)

    def test_new_doesnt_add_none(self):
        """test none doesnt work"""
        storage.new(None)
        self.assertNotIn("None", storage.all())

    def test_new_adds_multiple_objects(self):
        '''test that it adds multiple objects'''
        obj1 = BaseModel()
        obj2 = BaseModel()

        storage.new(obj1)
        storage.new(obj2)
        storage.save()

        key1 = f"{obj1.__class__.__name__}.{obj1.id}"
        key2 = f"{obj2.__class__.__name__}.{obj2.id}"

        self.assertIn(key1, storage.all())
        self.assertIn(key2, storage.all())

    def test_file_not_empty_after_saving(self):
        '''test that after saving file is no longer empty'''

        obj = BaseModel()
        storage.new(obj)
        storage.save()

        with open(self.test_file, "r") as f:
            data = json.load(f)

        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, data)

    def test_changes_persist_after_reloading(self):
        '''test saved info remains persistent'''
        obj = BaseModel()
        storage.new(obj)
        storage.save()

        with open(self.test_file, "r") as file:
            data1 = json.load(file)

        storage.reload()

        with open(self.test_file, "r") as file1:
            data2 = json.load(file1)


        self.assertEqual(data1, data2)

    def test_delete_method(self):
        '''tests that deleting removes object from storage'''
        obj = BaseModel()
        storage.new(obj)
        storage.save()

        with open(self.test_file, "r") as file:
            data = json.load(file)

        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, data)

        storage.delete(obj)
        storage.save()

        with open(self.test_file, "r") as file1:
            data1 = json.load(file1)

        self.assertNotIn(key, data1)




if __name__ == "__main__":
    unittest.main()
