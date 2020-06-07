from flask import Blueprint, render_template, request, redirect, url_for
from flask import current_app as app
from flask_login import login_required, current_user, logout_user
from .utils.login import try_login
from app.db import rdb, wdb, bdb

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates', static_folder='static') 


@admin_bp.route("/")
def display_default():
    return render_template("login.html")


@admin_bp.route("/login")
def display_login():
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
def display_info():
    return render_template("info.html")


@admin_bp.route("/browser")
@login_required
def display_browser():
    org_id = current_user.org_id

    data = rdb[org_id].all()
    bl = bdb[org_id].all()

    return render_template("reportbrowser.html", data=data, bl=bl, org_id=org_id)

@admin_bp.route("/settings")
@login_required
def display_settings():
    org_id = current_user.org_id
    wl = wdb[org_id].all()
    bl = bdb[org_id].all()
    return render_template("settings.html", wl=wl, bl=bl)