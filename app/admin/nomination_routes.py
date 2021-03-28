from app.models import *
from flask import Blueprint, request, render_template, redirect, url_for, current_app
from . import admin_blueprint
from app import is_development
from .nomination import CreateNominationForm

from sqlalchemy import func
from app import db,generate_uuid
import datetime

@admin_blueprint.route('/admin/nomination', methods=['GET'])
@admin_blueprint.route('/admin/nomination/<nomination_id>', methods=["GET", "POST"])
def list_nominations(nomination_id=None):
    if nomination_id is not None:
        print("Nomination detail")
        nomination = Nomination.query.filter(Nomination.id == nomination_id).first()
        return render_template('nomination_detail.html', nomination=nomination)
    else:
        print("nomination list")
        nominations = Nomination.query.all()
        return render_template('list_nomination.html', nominations=nominations)

@admin_blueprint.route('/admin/nomination/new', methods=['GET', 'POST'])
def create_nomination():
    form = CreateNominationForm()
    if request.method == 'POST':
        print("Post")
        if is_development():
            u = User.query.filter(User.jhed_id == 'dbelros1').first()
        else:
            u = User.query.filter(User.jhed_id == request.headers.get('USERPRINCIPALNAME')).first()
            if u is None:
                return "Bad bad bad", 500
    
        if form.validate_on_submit():
            f = form.data
            print("Form is valid")
            p = Project.query.filter(func.lower(Project.name) == func.lower(f.get('name'))).first()
            if p is None:
                print("Project does not exist")
                p = Project()
                p.id = generate_uuid()
                p.name = f.get('name')
                p.url = f.get('url')
                p.description = f.get('description')
                p.added_by = u.id
        
                db.session.add(p)
                db.session.commit()

                db.session.refresh(p)
                
            n = Nomination()
            n.user_id = u.id
            n.reason = f.get('description')
            n.project_id = p.id
            n.id = generate_uuid()

            db.session.add(n)
            db.session.commit()

            return redirect(url_for('admin_blueprint.list_nominations'))
        print("Form is not valid")
        print(form)
        return render_template("create_nomination_form.html", form=form)
    else:
        print("GET")
        return render_template(
            "create_nomination_form.html",
            form=form,
            template="form-template"
        )



