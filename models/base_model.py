#!/usr/bin/python3
'''class base model that defines all common attributes for other classes'''

from sqlalchemy.orm import declarative_base
import cmd
import datetime
import uuid
#from models import storage
from sqlalchemy import Column, Integer, String, DateTime
from os import getenv

if getenv("MWJ_TYPE_STORAGE") == "db":
    Base = declarative_base()
else:
    Base = object

class BaseModel:
    '''This is a class defining all common attributes for other classes'''
    """_instances = []"""

    if getenv("MWJ_TYPE_STORAGE") == "db":
        id = Column(String(60), primary_key=True, unique=True, nullable=False)
        created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """public instance attributes"""
        if kwargs:
            '''if kwargs not empty use each key of the dict as an attribute name'''
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ( "created_at", "updated_at") and isinstance(value, str):
                        setattr(self, key, datetime.datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)

            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
                self.created_at = datetime.datetime.now()
                self.updated_at = datetime.datetime.now()
                # storage.new(self)

        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()
            # storage.new(self)

    def __str__(self):
        """returns class name the id and dict"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        '''updates updated_At with the current datetime'''
        self.updated_at = datetime.datetime.now()
        from models import storage
        storage.new(self)
        storage.save()

    def to_dict(self):
        '''returns a dictionary containing all keys/values of __dict__ of instnce'''
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()

        obj_dict.pop("_sa_instance_state", None)

        return obj_dict

    def delete(self):
        '''deletes current instance from storage'''
        from models import storage
        storage.delete()

    @classmethod
    def all(cls):
        """returns all instances of this class"""
        return [str(obj) for key, obj in storage.all().items()
                if key.startswith(cls.__name__ + ".")]
