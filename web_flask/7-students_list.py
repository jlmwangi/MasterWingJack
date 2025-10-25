#!/usr/bin/python3
'''a script that starts a flask web application'''

from flask import Flask, render_template
import os
from models import storage
from models.student import Student


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    '''display hello masterWingJack'''
    return ("Hello Master_Wing_Jack!")

@app.route('/mwj', strict_slashes=False)
def mwj():
    '''display mwj'''
    return "MasterWingJack"

@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """display c followed by value of text"""
    if '_' in text:
        texts = text.replace('_', ' ')
        return "C" + ' ' + texts
    return "C" + ' ' + text

@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text="is cool"):
    """display python followed by value of text"""
    if '_' in text:
        texts = text.replace('_', ' ')
        return "Python" + ' ' + texts
    return "Python" + ' ' + text

@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """display n is a number"""
    return f"{n} is a number"

@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    '''display html page only if n is an integer'''
    return render_template('5-number.html', n=n)

@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    '''display html page only if n is a number'''
    return render_template('6-number_odd_or_even.html', n=n)

@app.route('/students_list', strict_slashes=False)
def students_list():
    '''display a html page containing students'''
    students = sorted(list(storage.all(Student).values()), key=lambda x : x.name)

    return render_template("7-students_list.html", students=students)


@app.teardown_appcontext
def remove_session(exception):
    '''remove current sqlalchemy session'''
    storage.close()



if __name__ == "__main__":
    host = os.environ.get('HOST', '0.0.0.0')
    port = os.environ.get('PORT', 5000)

    app.run(host=host, port=port, debug=True)
