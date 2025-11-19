#!/usr/bin/python3
'''index file'''

from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status')
def status():
    '''returns status of api'''
    return jsonify({'status': 'OK'})

@app_views.route('/stats')
def stats():
    '''retrieves the number of each objects by type'''
    from models.student import Student
    from models.lesson import Lesson
    from models.instructor import Instructor

    classnames = {
        "students": Student,
        'lessons': Lesson,
        'instructors': Instructor
    }

    stats_count = {}

    for key, value in classnames.items():
        stats_count[key] = storage.count(value)

    return jsonify(stats_count)
