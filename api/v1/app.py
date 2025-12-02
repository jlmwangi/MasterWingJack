#!/usr/bin/python3
'''flask main entry point'''

from flask import Flask, jsonify
from models import storage
from flask_cors import CORS
from api.v1.views import app_views

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

#from api.v1.views import app_views

app.register_blueprint(app_views)

@app.teardown_appcontext
def close_app(error=None):
    try:
        storage.close()
    except Exception as e:
        print("{}".format(e))

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Not Found"}), 404


if __name__ == "__main__":
    import os
    mwj_api_host = os.getenv('MWJ_API_HOST', '0.0.0.0')
    mwj_api_port = int(os.getenv('MWJ_API_PORT', 5000))

    app.run(host=mwj_api_host, port=mwj_api_port, threaded=True)
