#!/usr/bin/python3
""" initialize models """

from os import getenv

storage_type = getenv("MWJ_TYPE_STORAGE")

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
