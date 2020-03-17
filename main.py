#!/usr/bin/python3

"""
PhishDetector Backend
La Cañada Cybersecurity Club
"""

from flask import Flask, request, render_template, redirect
from flask.json import jsonify
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required
from waitress import serve as waitress_serve
from datetime import datetime, timedelta
import pytz
import dataset
from pickle import dump as pkl_dump, load as pkl_load
from json import load as json_load, dumps as json_dumps
from getpass import getpass
from login_utils import CredentialsManager

# Flask boilerplate
LISTEN_PORT = 8000
app = Flask(__name__)
cors = CORS(app, resources={r"/report/*": {"origins": "*"}})

db = dataset.connect('sqlite:///reports.db')
rdb = db.get_table('reports')

login_manager = LoginManager()

# Load salter-hasher
try:
    with open("data/credman.pkl", "rb") as credman_file:
        credman = pkl_load(credman_file)
except FileNotFoundError:
    credman = CredentialsManager()
    with open("data/credman.pkl", "wb+") as credman_file:
        pkl_dump(credman, credman_file)

# Load or create hashed credentials list (janky CLI way)
# TODO: Maybe make user-add page at some point :/
try:
    with open("data/logins.json", "r") as logins_file:
        logins = json_load(logins_file)

except FileNotFoundError:
    logins = []
    print("No users found. Please create a user.")
    username = input("Username: ")
    while True:
        password = getpass("Password: ")
        password_confirm = getpass("Confirm password: ")
        if password == password_confirm:
            break
        else:
            print("Passwords did not match. Please try again.")
    logins.append((username, credman.sh_pw(password)))
    print(f"User {username} added.")
    with open("data/logins.json", "w+") as logins_file:
        logins_file.write(json_dumps(logins))


# --- Server Listener actions ---

@app.route("/handle_report", methods=['POST', 'PUT'])
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