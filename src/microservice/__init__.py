# -*- encoding: utf-8 -*-
from importlib import import_module

from flask import Flask, jsonify, redirect, request

def register_extensions(_):
    # None for this microservice
    return


def register_default_routes(app, default_route):
    @app.route('/')
    def get_api():
        return redirect(default_route, code=302)

    @app.route('/health')
    def health():
        """Health endpoint."""
        return {"status":"ok"}

    @app.route('/headers', methods=['GET', 'POST', 'DELETE', 'PUT', 'OPTIONS'])
    def list_headers():
        """Returns a json with the request headers. (For DEBUG purposes)"""
        return jsonify({k: v for k, v in request.headers})

    @app.errorhandler(404)
    def not_found_error(error):
        return {'message': str(error)}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {'message': str(error)}, 500


def create_app(config):
    """Initializes the appliation

    REF:
        https://flask.palletsprojects.com/en/2.2.x/tutorial/factory/
        https://hackersandslackers.com/flask-application-factory/

    Args:
        config (Config): the Config object (cf. config.py)

    Returns:
        Flask: the newly created Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize Plugins
    register_extensions(app)

    # Registering Blueprints
    api_module = import_module('microservice.api.routes')
    app.register_blueprint(api_module.blueprint)

    # register default routes
    register_default_routes(app, api_module.blueprint.url_prefix)

    return app
