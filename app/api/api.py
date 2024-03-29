from flask import Blueprint, request, send_file, redirect
from flask_cors import CORS
from hashlib import sha256
import os.path
import re
from app.api.utils.discord import try_discord_send
from app.api.utils.functions import now
# from app.api.utils.rate_risk import rate_link
from app.db import rdb, bdb, wdb, tdb, opentrackdb, linktrackdb, assessmentdb
from app.admin.utils.credentials import load_organizations

def get_ext_key():
    return open(rel_path("../../extension_key.txt"), "r").read().strip()


api_bp = Blueprint('api_bp', __name__)
cors = CORS(api_bp, resources={r"/api/*": {"origins": "*"}})


@api_bp.route("/api/rate-risk/link", methods=['GET'])
def rate_risk_link():

    api_key = request.args.get('key')
    if sha256(api_key.encode()).hexdigest() != get_ext_key():
        return "Forbidden", 403

    url = request.args.get('url')
    return (rate_link(url))




@api_bp.route("/api/report", methods=['POST', 'PUT'])
def handle_report():

    data = request.get_json()
    api_key = data['key']
    if sha256(api_key.encode()).hexdigest() != get_ext_key():
        return "Forbidden", 403

    report_data = data['report_data']
    org_id = request.get_json()['org_id']
    report_data['timestamp'] = now()
    rdb.get_table(org_id).insert(report_data)
    return data, 200


@api_bp.route("/api/feedback", methods=['POST', 'PUT']) # keep as is
def handle_feedback():
    
    api_key = request.get_json()['key']
    if sha256(api_key.encode()).hexdigest() != get_ext_key():
        return "Forbidden", 403

    data = request.get_json()['data']
    data['timestamp'] = now()
    # fdb = db.get_table('feedback')
    # fdb.insert(data)
    try_discord_send(request.get_json()['discord'])
    return data, 200


@api_bp.route("/api/bug", methods=['POST', 'PUT']) # keep as is
def handle_bug():

    api_key = request.get_json()['key']
    if sha256(api_key.encode()).hexdigest() != get_ext_key():
        return "Forbidden", 403

    data = request.get_json()['data']
    data['timestamp'] = now()
    # bdb = db.get_table('bugs')
    # bdb.insert(data)
    try_discord_send(request.get_json()['discord'])
    return data, 200


@api_bp.route("/api/blacklist", methods=['GET'])
def get_blacklist():

    api_key = request.args.get('key')
    if sha256(api_key.encode()).hexdigest() != get_ext_key():
        return "Forbidden", 403

    args = request.args
    b1 = [item['address'] for item in bdb[args.get('org_id')].all()]
    return {
        'data': b1,
    }


@api_bp.route("/api/whitelist", methods=['GET'])
def get_whitelist():

    api_key = request.args.get('key')
    if sha256(api_key.encode()).hexdigest() != get_ext_key():
        return "Forbidden", 403

    args = request.args
    w1 = [item['address'] for item in wdb[args.get('org_id')].all()]
    return {
        'data': w1,
    }

@api_bp.route("/api/verify_email", methods=['GET'])
def verify_email():

    api_key = request.args.get('key')
    if sha256(api_key.encode()).hexdigest() != get_ext_key():
        return "Forbidden", 403


    target = request.args.get('address')

    # unclassified --> 0
    numrating = 0

    # whitelisted --> 1
    for item in wdb[request.args.get('org_id')].all():
        if re.match(item['address'], target):
            numrating = 1

    # blacklisted --> 2
    for item in bdb[request.args.get('org_id')].all():
        if re.match(item['address'], target):
            numrating = 2

    # test db --> 0 (pretend to be unclassified)
    for item in tdb[request.args.get('org_id')].all():
        if re.match(item['address'], target):
            numrating = 0
    
    return {'status': numrating}


@api_bp.route("/api/verify_emails", methods=['GET'])
def verify_emails():

    api_key = request.args.get('key')
    if sha256(api_key.encode()).hexdigest() != get_ext_key():
        return "Forbidden", 403

    targets = request.args.getlist('addresses')
    done = []
    ratings = {}

    for target in targets:

        if target not in done:

            # unclassified --> 0
            numrating = 0

            # whitelisted --> 1
            for item in wdb[request.args.get('org_id')].all():
                if re.match(item['address'], target):
                    numrating = 1

            # blacklisted --> 2
            for item in bdb[request.args.get('org_id')].all():
                if re.match(item['address'], target):
                    numrating = 2

            # test db --> 0 (pretend to be unclassified)
            for item in tdb[request.args.get('org_id')].all():
                if re.match(item['address'], target):
                    numrating = 0

            ratings[target] = numrating
            done.append(target)
    
    return ratings, 200


@api_bp.route("/api/get_org", methods=['GET'])
def get_organization():

    args = request.args
    api_key = args.get('key')
    if sha256(api_key.encode()).hexdigest() != get_ext_key():
        return "Forbidden", 403

    # json = request.get_json()
    # target_domain = json['address'].split("@")[1]
    # orgs = load_organizations()
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
    api_key = request.args.get('key')
    if sha256(api_key.encode()).hexdigest() != get_ext_key():
        return "Forbidden", 403

    orgs = load_organizations()

    for o in orgs:
        if o['id'] == request.args['id']:
            return {
                'support_emails': o['support_emails']
            }, 200
    return {} 


# Tracking pixels 
# NOTE: MUST have org_id assessment_id, and email

@api_bp.route("/api/opentrack", methods=['GET'])
def get_img_opentrack():
    assessment_id = request.args['assessment_id']
    org_id = request.args['org_id']
    if not assessmentExists(org_id, assessment_id):
        return "Forbidden", 403
    dbitem = {
        'assessment_id': assessment_id,
        'address': request.args['address']
    }
    table = opentrackdb.get_table(org_id)

    redundant = False
    for item in table:
        if dbitem['address'] == item['address']:
            redundant = True
            # return "Log Conflict", 409

    if not redundant:
        table.insert(dbitem)

    return send_file(rel_path('./img/pixel_white_1x1.png'), mimetype='image/png')


@api_bp.route("/api/linktrack", methods=['GET'])
def get_img_linktrack():
    assessment_id = request.args['assessment_id']
    org_id = request.args['org_id']
    if not assessmentExists(org_id, assessment_id):
        return "Forbidden", 403
    dbitem = {
        'assessment_id': assessment_id,
        'address': request.args['address']
    }
    table = linktrackdb.get_table(org_id)

    redundant = False
    for item in table:
        if dbitem['address'] == item['address']:
            redundant = True
            # return "Log Conflict", 409

    if not redundant:
        table.insert(dbitem)

    # no longer need to send img pixel for this link, instead redirect to phished.html on club site
    # return send_file(rel_path('./img/pixel_white_1x1.png'), mimetype='image/png')
    return redirect("https://lchs-cybersecurity.github.io/phished")


def rel_path(string):
    return os.path.join(os.path.dirname(__file__), string)

def assessmentExists(org_id: str, assessment_id: str):
    table = assessmentdb.get_table(org_id)
    for item in table:
        if item['assessment_id'] == assessment_id:
            return True
    return False