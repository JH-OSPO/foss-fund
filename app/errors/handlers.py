from flask import Blueprint, render_template

error_blueprint = Blueprint('errors', __name__)

@error_blueprint.app_errorhandler(403)
def not_authorized(e):
    return render_template('errors/403.html'), 403

@error_blueprint.app_errorhandler(404)
def throw_404(e):
    return render_template('errors/404.html'), 404

@error_blueprint.app_errorhandler(500)
def throw_500(e):
    return render_template('errors/500.html'), 500
