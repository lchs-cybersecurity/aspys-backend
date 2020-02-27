#!/usr/bin/python3

"""
PhishDetector Backend
La Cañada Cybersecurity Club
"""

from flask import Flask, request, render_template
from flask.json import jsonify
from waitress import serve as waitress_serve
from db_utils import ReportDatabase

LISTEN_PORT = 8000
app = Flask(__name__)

rdb = ReportDatabase("reports.db")
rdb.create_db()

# Flask: Listen for PUT https request from extensions
@app.route("/report", methods=['POST', 'PUT'])
def handle_report():
    rdb.new_entry(request.args["sender"], request.args["content"])

# Flask: Listen for local GET request, return DB item dict
@app.route("/items", methods=['GET'])
def get_items():
    return jsonify(rdb.items())
    # CURSED CODE, NO TOUCH
    # http_put(f"http://localhost:{LISTEN_PORT}")

@app.route("/delete", methods=['POST', 'PUT'])
def delete_item():
    rdb.delete(request.args["id"])

@app.route("/")
def display_db_browser():
    with open("pages/reportbrowser.html") as dbb_file:
        dbb_string = ""
        for line in dbb_file:
            dbb_string += str(line)
        return dbb_string

# NOTE: `app.run` is for testing only, NOT deployment.
# app.run(debug=True, )
waitress_serve(app, host='0.0.0.0', port=LISTEN_PORT)
