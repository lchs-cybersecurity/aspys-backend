from flask import Flask, render_template
from flask_assets import Environment
from .admin.utils.login import login_manager
from .assets import compile_static_assets
from werkzeug.serving import run_simple
from os import getenv
from waitress import serve as waitress_serve


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    assets = Environment()
    assets.init_app(app)
    login_manager.init_app(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    with app.app_context():
        from .admin import admin
        from .api import api

        app.register_blueprint(admin.admin_bp)
        app.register_blueprint(api.api_bp)

        compile_static_assets(assets)

        return app

def run_app(app):
    host = getenv('HOST')
    port = int(getenv('PORT'))
    if getenv('FLASK_ENV') == 'production':
        waitress_serve(app, host=host, port=port, ssl_context='adhoc')
    else:
        run_simple(host, port, app)