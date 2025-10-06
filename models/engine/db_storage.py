#!/usr/bin/python3
"""database storage"""

from sqlalchemy import create_engine
from os import getenv
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
"""from models.student import Student
from models.lesson import Lesson
from models.instructor import Instructor"""


load_dotenv()

mwj_user = getenv("MWJ_MYSQL_USER")
mwj_pwd = getenv("MWJ_MYSQL_PWD")
mwj_host = getenv("MWJ_MYSQL_HOST")
mwj_db = getenv("MWJ_MYSQL_DB")
mwj_env = getenv("MWJ_ENV")


"""classnames = {
        "Student": Student,
        "Lesson": Lesson,
        "Instructor": Instructor
        }"""

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """initialize db storage"""
        mwj_env = getenv("MWJ_ENV", "dev")

        if mwj_env == "test":
            """Base.metadata.drop_all(self.__engine)"""
            self.__engine = create_engine("sqlite:///:memory:", echo=False)
        else:
            self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                .format(mwj_user, mwj_pwd, mwj_host, mwj_db),
                pool_pre_ping=True)

        #if mwj_env == "test":
         #Base.metadata.drop_all(self.__engine)
        #else:
         #   Base.metadata.create_all(self.__engine)

    def all(self, cls=None):
        """query all objs depending on class name"""
        obj_dict = {}
        if cls:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = f"{obj.__class__.__name__}.{obj.id}"
                obj_dict[key] = obj
            return obj_dict
        else:
            from models.student import Student
            from models.lesson import Lesson
            from models.instructor import Instructor
            classnames = {
                    "Student": Student,
                    "Lesson": Lesson,
                    "Instructor": Instructor
                    }
            for classname, class_type in classnames.items():
                objs = self.__session.query(class_type).all()
                for obj in objs:
                    key = f"{classname}.{obj.id}"
                    obj_dict[key] = obj
            return obj_dict

    def new(self, obj):
        """adds an object to current database session"""
        self.__session.add(obj)
        self.save()

    def save(self):
        """commit all changes of current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from current database session"""
        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """create tables in the database, create current session"""
        from models.student import Student
        from models.lesson import Lesson
        from models.instructor import Instructor
        from models.base_model import Base

        Base.metadata.create_all(self.__engine)

        session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session = session()

    def close(self):
        """close current session"""
        self.__session.close()
