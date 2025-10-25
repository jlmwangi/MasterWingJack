#!/usr/bin/python3
'''a script that starts a flask web application'''

from flask import Flask
import os


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    '''display hello masterWingJack'''
    return ("Hello Master_Wing_Jack!")


if __name__ == "__main__":
    host = os.environ.get('HOST', '0.0.0.0')
    port = os.environ.get('PORT', 5000)

    app.run(host=host, port=port, debug=True)
