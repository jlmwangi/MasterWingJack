#!/usr/bin/python3
'''test class Base model'''


import unittest
from models.base_model import BaseModel
import datetime
import uuid


class TestBaseModel(unittest.TestCase):
    '''create your inputs
       run your inputs using your method capturing output
       compare output with expected result'''
    def test_init_with_kwargs(self):
        '''test that the method takes args and kw args'''
        kwargs_inputs = {
                "key": "value",
                "k": "v",
                "keyy": "valuee"
        }

        obj = BaseModel(**kwargs_inputs)

        self.assertEqual(obj.key, "value")
        self.assertEqual(obj.k, "v")
        self.assertEqual(obj.keyy, "valuee")

    def test_init_without_kwargs(self):
        '''test that the init method also takes no arguments'''
        obj = BaseModel()
        
        self.assertTrue(hasattr(obj, "id"))
        self.assertTrue(hasattr(obj, "created_at"))
        self.assertTrue(hasattr(obj, "updated_at"))

        self.assertIsInstance(obj.updated_at, datetime.datetime)
        self.assertIsInstance(obj.created_at, datetime.datetime)

    def test_str_method(self):
        '''test that the str method returns a string in the order it should'''
        obj = BaseModel()
        result = str(obj)

        self.assertEqual(result, f"[{obj.__class__.__name__}] ({obj.id}) {obj.__dict__}")

    def test_save_method(self):
        '''tests that the updated at time changes'''
        obj = BaseModel()
        old_time = obj.updated_at
        obj.save()

        self.assertGreater(obj.updated_at, old_time)

    def test_to_dict(self):
        """test to dict method"""
        obj = BaseModel()
        result = obj.to_dict()

        self.assertIsInstance(result, dict)
        self.assertIn("id", result)
        self.assertIn("created_at", result)




if __name__ == "__main__":
    unittest.main()
