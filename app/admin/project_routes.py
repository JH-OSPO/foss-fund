from flask import Blueprint, request, render_template, redirect, url_for, current_app, flash, abort
from app.models import *
from sqlalchemy import func
from . import admin_blueprint
from .project import ProjectForm
from app import db, generate_uuid, is_development

@admin_blueprint.route('/admin/project', methods=['GET', 'POST'])
@admin_blueprint.route('/admin/project/<project_id>', methods=['GET', 'POST'])
def list_projects(project_id=None):
    form = ProjectForm()
    if request.method == 'GET':
        if project_id is not None:
            return "test", 500  # fix me
        else:
            projects = Project.query.all()
            return render_template('list_projects.html', projects=projects, form=form)
    elif request.method == 'POST':
        if is_development():
            u = User.query.filter(User.jhed_id == 'dbelros1').first()
        else:
            u = User.query.filter(User.jhed_id == request.headers.get('USERPRINCIPALNAME')).first()

        f = form.data
        if project_id is None:
            project = Project.query.filter(func.lower(Project.name) == func.lower(f.get('name'))).first()
            if project is None:
                project = Project()
                project.id = generate_uuid()
                project.name = f.get('name')
                project.url = f.get('url')
                project.description = f.get('description')
                project.user_id = u.id

                db.session.add(project)
                db.session.commit()


                db.session.refresh(project)

                return redirect(url_for('admin_blueprint.list_projects'))
        else:
            return "I don't know what to do here yet"
