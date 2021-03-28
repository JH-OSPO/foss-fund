from flask import Blueprint

admin_blueprint = Blueprint('admin_blueprint', __name__)

from . import campaign_routes
from . import nomination_routes
from . import user_routes
from . import project_routes

from . import routes
