#!/usr/bin/python3

"""
PhishDetector Backend
La Cañada Cybersecurity Club
"""

from flask import Flask, request, render_template, redirect, session
from flask.json import jsonify
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required
import dataset
import requests
from json import load as json_load, dumps as json_dumps
from getpass import getpass
from os import urandom
from werkzeug.serving import run_simple

from login_utils import load_credentialsmanager, load_organizations
from other_utils import *

# Load config
with open("config.json", "r+", encoding="utf-8") as config_file:
    config = dict(json_load(config_file))
    LISTEN_PORT = config["port"]

    # Generate unique client secret
    if config["secret_key"] == "":
        config["secret_key"] = str(urandom(32))
        config_file.seek(0)
        config_file.write(json_dumps(config))
        config_file.truncate()

# Flask boilerplate
app = Flask(__name__)
app.config['TESTING'] = False
app.secret_key = config["secret_key"]
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

db = dataset.connect('sqlite:///reports.db')
rdb = db.get_table('reports') 
bdb = db.get_table('blacklist') 
wdb = db.get_table('whitelist') 

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "/"
login_manager.init_app(app)

active_users = []
class User(UserMixin):
    userid = ""
    
    def __init__(self, new_id: str):
        self.userid = new_id
    
    def get_id(self):
        return self.userid

@login_manager.user_loader
def load_user(userid: str):
    # return active_users[int(userid)]
    return User(userid)


# Load salter-hasher
credman = load_credentialsmanager()

# Load or create hashed credentials list (janky CLI way)
organizations = []
logins = load_organizations()

# --- Server Listener actions ---

@app.route("/api/report", methods=['POST', 'PUT'])
def handle_report():
    data = request.get_json()['data']
    data['timestamp'] = now()
    rdb.insert(data)
    return data, 200 # 200 indicates success to client


@app.route("/api/feedback", methods=['POST', 'PUT']) # keep as is
def handle_feedback():
    data = request.get_json()['data']
    data['timestamp'] = now()
    fdb = db.get_table('feedback')
    fdb.insert(data)
    tryDiscordSend(request.get_json()['discord'])
    return data, 200


@app.route("/api/bug", methods=['POST', 'PUT']) # keep as is
def handle_bug():
    data = request.get_json()['data']
    data['timestamp'] = now()
    bdb = db.get_table('bugs')
    bdb.insert(data)
    tryDiscordSend(request.get_json()['discord'])
    return data, 200


@app.route("/handle_login", methods=['POST'])
def handle_login():
    username = request.form.get("username")
    password = request.form.get("password")
    for login in logins:
        if username == login["user"] and credman.sh_pw(password) == login["sh_pw"]:
            user = User(str(len(active_users)))
            active_users.append(user)
            login_user(user)
            print(f"Logged in user {username}.")
            return redirect("/browser")
        else:
            print("Login failed.")
            return redirect("/")


@app.route("/delete", methods=['POST', 'PUT']) # per-org
def delete_item(): 
    json = request.get_json() 

    print(json)  

    rdb.delete(id=json.get('id')) 

    return json, 200

@app.route("/blacklist", methods=['POST', 'PUT']) # per-org
def blacklist_address(): 
    json = request.get_json() 

    print(json) 

    bdb.upsert(json, ['address']) 

    return json, 200

@app.route("/whitelist", methods=['POST', 'PUT']) # per-org
def whitelist_address(): 
    json = request.get_json() 

    print(json) 

    wdb.insert(json) 

    return json, 200

@app.route("/api/get_blacklist") # per-org
def get_blacklist(): 
    b1 = [item['address'] for item in bdb.all()] 

    return {
        'data': b1, 
    } 

@app.route("/favicon.ico")
def favicon(): 
    return {}, 200

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/info")
def display_info():
    return render_template("info.html")

@app.route("/")
def display_login():
    return render_template("login.html")

@app.route("/browser")
@login_required
def display_browser():
    data = rdb.all() 
    bl = bdb.all() 

    return render_template("reportbrowser.html", data=data, bl=bl) 

run_simple('0.0.0.0', LISTEN_PORT, app, ssl_context='adhoc')
