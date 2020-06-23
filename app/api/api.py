from flask import Blueprint, request
from flask_cors import CORS
from app.api.utils.discord import try_discord_send
from app.api.utils.functions import now
#from app.api.utils.rate_risk import rate_link
from app.db import rdb, bdb, wdb
from app.admin.utils.credentials import load_organizations


api_bp = Blueprint('api_bp', __name__)
"""
TODO:
Due to nature of Chrome extensions, we have to accept
all origins. However it would be unsafe to accept all,
so we need to add a token/key check.
- Trinity
"""
cors = CORS(api_bp, resources={r"/api/*": {"origins": "*"}})


@api_bp.route("/api/rate-risk/link", methods=['GET'])
def rate_risk_link():
    url = request.args.get('url')
    return (rate_link(url))



@api_bp.route("/api/report", methods=['POST', 'PUT'])
def handle_report():
    data = request.get_json()['data']
    org_id = request.get_json()['org_id']
    data['timestamp'] = now()
    rdb[org_id].insert(data)
    return data, 200


@api_bp.route("/api/feedback", methods=['POST', 'PUT']) # keep as is
def handle_feedback():
    data = request.get_json()['data']
    data['timestamp'] = now()
    # fdb = db.get_table('feedback')
    # fdb.insert(data)
    try_discord_send(request.get_json()['discord'])
    return data, 200


@api_bp.route("/api/bug", methods=['POST', 'PUT']) # keep as is
def handle_bug():
    data = request.get_json()['data']
    data['timestamp'] = now()
    # bdb = db.get_table('bugs')
    # bdb.insert(data)
    try_discord_send(request.get_json()['discord'])
    return data, 200


@api_bp.route("/api/delete", methods=['POST', 'PUT'])
def delete_item():
    json = request.get_json()
    rdb[json.get('org_id')].delete(id=json.get('id'))
    return json, 200


@api_bp.route("/api/blacklist", methods=['GET'])
def get_blacklist():
    args = request.args
    b1 = [item['address'] for item in bdb[args.get('org_id')].all()]
    return {
        'data': b1,
    }


@api_bp.route("/api/blacklist", methods=['POST', 'PUT'])
def blacklist_address():
    json = request.get_json()
    bdb[json.get('org_id')].upsert(json, ['address'])
    return json, 200

@api_bp.route("/api/set_blacklist", methods=['POST', 'PUT']) 
def set_blacklist(): 
    json = request.get_json() 

    print(json) 
    
    org_id = json.get('org_id') 
    blacklist = [{
        'address': address, 
        'org_id': org_id, 
    } for address in json['list']] 
    
    table = bdb[org_id] 

    print(repr(blacklist)) 

    table.delete() 

    table.insert_many(blacklist) 

    return json, 200

@api_bp.route("/api/whitelist", methods=['GET'])
def get_whitelist():
    args = request.args
    w1 = [item['address'] for item in wdb[args.get('org_id')].all()]
    return {
        'data': w1,
    }

@api_bp.route("/api/whitelist", methods=['POST', 'PUT'])
def whitelist_address():
    json = request.get_json()
    wdb[json.get('org_id')].insert(json)
    return json, 200

@api_bp.route("/api/set_whitelist", methods=['POST', 'PUT']) 
def set_whitelist(): 
    json = request.get_json() 
    org_id = json.get('org_id') 
    whitelist = [{
        'address': address, 
        'org_id': org_id, 
    } for address in json['list']] 
    
    table = wdb[org_id] 

    print(repr(whitelist)) 

    table.delete() 

    table.insert_many(whitelist) 

    return json, 200

@api_bp.route("/api/get_org", methods=['GET'])
def get_organization():
    # json = request.get_json()
    # target_domain = json['address'].split("@")[1]
    # orgs = load_organizations()
    args = request.args
    target_domain = args.get('address').split("@")[1]
    orgs = load_organizations()  

    ID = '' 

    for o in orgs:
        if target_domain in o['domains']:
            ID = o['id'] 
            
            break 
    
    return {
        'ID': ID, 
    }, 200

@api_bp.route("/api/get_support_emails", methods=['GET'])
def get_support_emails():
    orgs = load_organizations()

    for o in orgs:
        if o['id'] == request.args['id']:
            return {
                'support_emails': o['support_emails']
            }, 200
    return {}
