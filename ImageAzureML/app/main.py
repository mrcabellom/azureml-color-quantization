from flask import Flask, render_template
from image_module.controllers import IMAGE_MOD

FLASK_APP = Flask(__name__, instance_relative_config=True)
FLASK_APP.config.from_object('config')
FLASK_APP.config.from_pyfile('config.py')

@FLASK_APP.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error), 404

FLASK_APP.register_blueprint(IMAGE_MOD)
