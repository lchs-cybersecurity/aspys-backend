#!/usr/bin/python3

"""
PhishDetector Backend
La Cañada Cybersecurity Club
"""

from flask import Flask, request, render_template
from waitress import serve as waitress_serve
from db_utils import ReportDatabase

LISTEN_PORT = 8000
app = Flask(__name__)

rdb = ReportDatabase("reports.db")
rdb.create()

# Flask: Listen for PUT https request from extensions
@app.route("/report", methods=['POST', 'PUT'])
def handle_report():
    rdb.new_entry(request.args["sender"], request.args["content"])

@app.route("/")
def display_db_browser():
    with open("db_browser.html") as dbb_file:
        dbb_string = ""
        for line in dbb_file:
            dbb_string += str(line)
        return dbb_string

# NOTE: `app.run` is for testing only, NOT deployment.
# app.run(debug=True, )
waitress_serve(app, host='0.0.0.0', port=LISTEN_PORT)
