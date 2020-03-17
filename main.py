#!/usr/bin/python3

"""
PhishDetector Backend
La Cañada Cybersecurity Club
"""

from flask import Flask, request, render_template
from flask.json import jsonify
from flask_cors import CORS
from waitress import serve as waitress_serve
from datetime import datetime, timedelta
import pytz
import dataset

LISTEN_PORT = 8000
app = Flask(__name__)
cors = CORS(app, resources={r"/report/*": {"origins": "*"}})

db = dataset.connect('sqlite:///reports.db')
rdb = db.get_table('reports')

# Flask: Listen for PUT https request from extensions
@app.route("/report", methods=['POST', 'PUT'])
def handle_report():
    data = request.get_json()
    data['timestamp'] = datetime.now(pytz.utc)
    rdb.insert(data)
    return data, 200 # 200 indicates success to client

# Flask: Listen for local GET request, return DB item dict
@app.route("/items", methods=['GET'])
def get_items():
    return jsonify(rdb.items())

@app.route("/delete", methods=['POST', 'PUT'])
def delete_item():
    rdb.delete(receiver=request.args["receiver"])

@app.route("/")
def display_login():
    return render_template("login.html")

@app.route("/browser")
def display_browser():
    return render_template("reportbrowser.html")

waitress_serve(app, host='0.0.0.0', port=LISTEN_PORT)