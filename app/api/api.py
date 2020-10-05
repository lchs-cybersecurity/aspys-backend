from flask import Blueprint, request
from flask_cors import CORS
from hashlib import sha256
import os.path
from app.api.utils.discord import try_discord_send
from app.api.utils.functions import now
# from app.api.utils.rate_risk import rate_link
from app.db import rdb, bdb, wdb
from app.admin.utils.credentials import load_organizations

def get_ext_key():
    return open(rel_path("../../extension_key.txt"), "r").read().strip()


api_bp = Blueprint('api_bp', __name__)
cors = CORS(api_bp, resources={r"/api/*": {"origins": "*"}})


@api_bp.route("/api/rate-risk/link", methods=['GET'])
def rate_risk_link():
    url = request.args.get('url')
    api_key = request.args.get('key')
    return (rate_link(url)) if sha256(api_key.encode()).hexdigest() == get_ext_key() else 400




@api_bp.route("/api/report", methods=['POST', 'PUT'])
def handle_report():
    data = request.get_json()
    api_key = data['key']
    report_data = data['report_data']
    org_id = request.get_json()['org_id']
    report_data['timestamp'] = now()
    rdb().get_table(org_id).insert(report_data)
    return data, 200 if sha256(api_key.encode()).hexdigest() == get_ext_key() else 400


@api_bp.route("/api/feedback", methods=['POST', 'PUT']) # keep as is
def handle_feedback():
    data = request.get_json()['data']
    api_key = request.get_json()['key']
    data['timestamp'] = now()
    # fdb = db.get_table('feedback')
    # fdb.insert(data)
    try_discord_send(request.get_json()['discord'])
    return data, 200 if sha256(api_key.encode()).hexdigest() == get_ext_key() else 400


@api_bp.route("/api/bug", methods=['POST', 'PUT']) # keep as is
def handle_bug():
    data = request.get_json()['data']
    api_key = request.get_json()['key']
    data['timestamp'] = now()
    # bdb() = db.get_table('bugs')
    # bdb().insert(data)
    try_discord_send(request.get_json()['discord'])
    return data, 200 if sha256(api_key.encode()).hexdigest() == get_ext_key() else 400


@api_bp.route("/api/blacklist", methods=['GET'])
def get_blacklist():
    args = request.args
    api_key = request.args.get('key')
    b1 = [item['address'] for item in bdb()[args.get('org_id')].all()]
    return {
        'data': b1,
    } if sha256(api_key.encode()).hexdigest() == get_ext_key() else 400


@api_bp.route("/api/whitelist", methods=['GET'])
def get_whitelist():
    args = request.args
    api_key = request.args.get('key')
    w1 = [item['address'] for item in wdb()[args.get('org_id')].all()]
    return {
        'data': w1,
    } if sha256(api_key.encode()).hexdigest() == get_ext_key() else 400


@api_bp.route("/api/get_org", methods=['GET'])
def get_organization():
    # json = request.get_json()
    # target_domain = json['address'].split("@")[1]
    # orgs = load_organizations()
    args = request.args
    api_key = args.get('key')
    target_domain = args.get('address').split("@")[1]
    orgs = load_organizations()  

    ID = '' 

    for o in orgs:
        if target_domain in o['domains']:
            ID = o['id'] 
            
            break 
    
    return {
        'ID': ID, 
    }, 200 if sha256(api_key.encode()).hexdigest() == get_ext_key() else 400

@api_bp.route("/api/get_support_emails", methods=['GET'])
def get_support_emails():
    api_key = request.args.get('key')
    orgs = load_organizations()

    for o in orgs:
        if o['id'] == request.args['id']:
            return {
                'support_emails': o['support_emails']
            }, 200 if sha256(api_key.encode()).hexdigest() == get_ext_key() else 400
    return {} 

def rel_path(string):
    return os.path.join(os.path.dirname(__file__), string)
