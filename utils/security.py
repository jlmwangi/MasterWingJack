#!/usr/bin/python3
'''password hashing and checking functions'''

import bcrypt

def hash_password(password: str) -> str:
    '''hash a plain text password using bcrypt'''
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def check_password(password: str, hashed_password: str) -> str:
    """verify a password against a hashed password"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
