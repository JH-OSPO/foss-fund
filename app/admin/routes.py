from flask import request, abort, session, render_template
from app.models import User
from . import admin_blueprint
from app.permissions import is_allowed
from app import is_development

import jsonpickle
import os

@admin_blueprint.before_request
def permission_check():
    if is_development():
        u = User.query.filter(User.jhed_id == 'dbelros1').first()
    else:
        u = User.query.filter(User.jhed_id == request.headers.get('USERPRINCIPALNAME')).first()

    print(u.jhed_id)
    if not u.administrator:
            print(u.administrator)
            abort(403)
            return False
    return

@admin_blueprint.route('/admin', methods=["GET"])
def admin_home():
    return render_template('admin_index.html')
