from flask import current_app as app
from flask_assets import Bundle

def compile_static_assets(assets):
    assets.auto_build = True
    assets.debug = False

    common_css = Bundle('src/css/*.css', filters='cssmin', output='dist/css/style.css')
    # common_js = Bundle('src/js/*.js', filters='jsmin', output='dist/css/scripts.js')
    
    assets.register('common_css', common_css)
    # assets.register('common_js', common_js)

    if app.config['FLASK_ENV'] == 'development':
        common_css.build()
        # common_js.build()

    return assets