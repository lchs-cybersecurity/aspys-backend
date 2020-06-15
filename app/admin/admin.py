from flask import Blueprint, render_template, request, redirect, url_for
from flask import current_app as app
from flask_login import login_required, current_user, logout_user
from .utils.login import try_login
from app.db import rdb, wdb, bdb
from .utils.credentials import load_organizations, write_organizations

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates', static_folder='static') 


@admin_bp.route("/")
def display_default():
    if current_user.is_authenticated:
        return redirect("/browser")
    return render_template("login.html")


@admin_bp.route("/login")
def display_login():
    if current_user.is_authenticated:
        return redirect("/browser")
    return render_template("login.html")


@admin_bp.route("/login", methods=['POST'])
def handle_login():
    username = request.form.get("username")
    password = request.form.get("password")
    success = try_login(username, password)
    if (success):
        return redirect("/browser")
    return render_template("login.html", error='Check the orgainzation username and/or password.')


@admin_bp.route("/logout", methods=['GET'])
@login_required
def handle_logout():
    logout_user()
    return redirect(url_for("admin_bp.display_login"))


@admin_bp.route("/info")
@login_required
def display_info():
    return render_template("info.html")


@admin_bp.route("/browser")
@login_required
def display_browser():
    org_id = current_user.org_id

    data = rdb[org_id].all()
    bl = bdb[org_id].all()

    return render_template("reportbrowser.html", data=data, bl=bl, org_id=org_id)

@admin_bp.route("/settings", methods=['GET'])
@login_required
def display_settings():
    org_id = current_user.org_id
    wl = wdb[org_id].all()
    bl = bdb[org_id].all()

    orgs = load_organizations()
    for i in orgs:
        if i['id'] == org_id:
            support_emails_str = ""
            support_emails = i["support_emails"]
            for i in support_emails:
                support_emails_str += i
                if support_emails.index(i) + 1 < len(support_emails):
                    support_emails_str += ", "

    return render_template("settings.html", wl=wl, bl=bl, 
    support_emails_str=support_emails_str)

@admin_bp.route("/settings", methods=['POST', 'PUT'])
# @login_required
def write_settings():
    if not current_user.is_authenticated:
        return 403
    orgs = load_organizations()
    org_id = current_user.org_id

    # TODO: Come up with proper (EASY AND STREAMLINED) way to display & write to WL/BL
    # wl = wdb[org_id].all()
    # bl = bdb[org_id].all()

    support_emails_str = str(request.form.get("support_emails"))

    support_emails = []
    for e in [i.strip() for i in support_emails_str.split(",")]:
        support_emails.append(e)

    for o in orgs:
        if o["id"] == org_id:
            o["support_emails"] = support_emails

    write_organizations(orgs)

    # NOTE: Return a redirect for now, unless we want to reimplement/move stringification stuff later
    return redirect("/settings")