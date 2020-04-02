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
import dataset
import requests
from pickle import dump as pkl_dump, load as pkl_load
from json import load as json_load, dumps as json_dumps
from getpass import getpass
from login_utils import CredentialsManager
from other_utils import *

# Flask boilerplate
LISTEN_PORT = 8000
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

db = dataset.connect('sqlite:///reports.db')
rdb = db.get_table('reports')
fdb = db.get_table('feedback')

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

@app.route("/api/report", methods=['POST', 'PUT'])
def handle_report():
    data = request.get_json()
    data['timestamp'] = now()
    rdb.insert(data)
    return data, 200 # 200 indicates success to client


@app.route("/api/feedback", methods=['POST', 'PUT'])
def handle_feedback():
    data = request.get_json()
    data['timestamp'] = now()
    fdb.insert(data)
    try:
        with open("config.json", "r") as config_file:
            config = json_load(config_file)
        if "discord_webhook" in config:
            discord_webhook = config['discord_webhook']
            embed_fields = []
            for key, field in data.items():
                print(field)
                embed_fields.append({
                    "name":limit_str(field["label"], 256),
                    "value":limit_str(field["value"], 1024)
                })
            message = {
                "embeds": [{
                    "color": "53622",
                    "title": "Feedback",
                    "timestamp": str(now()),
                    "fields": embed_fields
                }]
            }
            response = requests.post(discord_webhook, json=message)
    except Exception as e:
        print(f"Exception: {e}")
        return data, 400
    return data, 200


@app.route("/handle_login", methods=['POST'])
def handle_login():
    username = request.form.get("username")
    password = request.form.get("password")

    login_success = credman.check_credentials(username, password, logins)

    # TEMP TEST
    print(f"User: {username}\nPass: {password}")

    # change login actions
    return redirect("/")


@app.route("/delete", methods=['POST', 'PUT'])
def delete_item():
    rdb.delete(receiver=request.args.get("receiver"))


@app.route("/")
def display_login():
    return render_template("login.html")


@app.route("/browser/<receiver>")
def display_browser(receiver):
    data = rdb.find(receiver=receiver)
    return render_template("reportbrowser.html", data=data)

waitress_serve(app, host='0.0.0.0', port=LISTEN_PORT)