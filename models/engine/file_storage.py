#!/usr/bin/python3
'''a class file storage that serializes instances to a json file and vice versa'''

import json
import uuid
from datetime import datetime


class FileStorage:
    '''serializes to json file and deserializes to instances'''
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        '''returns the dictionary --objects'''
        obj_dict = {}
        if cls:
            for key, obj in self.__objects.items():
                if isinstance(obj, cls):
                    obj_dict[key] = obj
            return obj_dict
        return self.__objects

    def new(self, obj):
        '''sets in __objects the obj with key <obj class name>.id'''
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        '''serialises objects to the json file'''
        with open(self.__file_path, "w") as f:
            obj_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
            json.dump(obj_dict, f)

    def reload(self):
        """deserializes the json file to __objects"""
        try:
            with open(self.__file_path, "r") as f:
                obj_dict = json.load(f)
                from models.base_model import BaseModel
                from models.student import Student
                from models.instructor import Instructor
                from models.lesson import Lesson
                class_names = {
                    'BaseModel': BaseModel,
                    'Student': Student,
                    'Instructor': Instructor,
                    'Lesson': Lesson
                }
                for key, val in obj_dict.items():
                    class_name = val.get('__class__')
                    if class_name in class_names:
                        cls = class_names[class_name]
                        obj_data = {k: v for k, v in val.items() if k != '__class__'}
                        self.__objects[key] = cls(**obj_data)

        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        '''deletes obj from __objects if its contained there'''
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            del self.__objects[key]

    def close(self):
        '''call reload method to desirialize objects'''
        self.reload()

    def get(self, cls, id):
        """retrieves one object from storage"""
        if cls is None or id is None:
            return None
        
        key = f"{cls.__name__}.{id}"
        return self.__objects.get(key)

    def count(self, cls=None):
        '''count number of objects in storage'''
        if cls is None:
            return len(self.__objects)

        return len({
            key: obj for key, obj in self.__objects.items()
            if key.startswith(cls.__name__ + ".")
        })
