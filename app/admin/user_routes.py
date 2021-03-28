from app.models import User, Nomination
from flask import Blueprint, render_template, redirect, request, abort
from . import admin_blueprint

from app import db, generate_uuid
from .user import CreateUserForm, UpdateUserForm


@admin_blueprint.route('/admin/user', methods=['GET'])
@admin_blueprint.route('/admin/user/<user_id>', methods=['GET', 'POST'])
def list_users(user_id=None):
    form = UpdateUserForm()
    if user_id is None:
        users = User.query.all()
        return render_template('list_users.html', users=users)
    else: 
        if request.method == 'GET':
            u = User.query.filter(User.id == user_id).first()
            if u is not None:
                nominations = Nomination.query.filter(Nomination.user_id == u.id)
                return render_template('user_detail.html', user=u, form=form, nominations=nominations, template="form-template")
            else:
                abort(404)
        elif request.method == 'POST':
            form = UpdateUserForm()
            f = form.data
            print(f)
            u = User.query.filter(User.id == user_id).first()
            u.administrator = f.get('is_admin')
            db.session.commit()
            return("Yay")
