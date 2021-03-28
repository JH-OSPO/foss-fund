from flask import Blueprint, request, current_app, redirect, Response, url_for
from app import generate_uuid, is_development
from app.models import *
from sqlalchemy import func
from .nomination import UserNominationForm
from flask_cors import CORS

nominate_blueprint = Blueprint('nominate', __name__)
CORS(nominate_blueprint)


@nominate_blueprint.route('/nominate', methods=['GET', 'POST'])
def nomination():
    form = UserNominationForm()
    if request.method == 'GET':
        return render_template('nominate.html', form=form, template="form-template")
    
    elif request.method == 'POST':
        if form.validate_on_submit():
            if is_development():
                user = User.query.filter(User.jhed_id == 'dbelros1').first()
            else:
                user = User.query.filter(User.jhed_id == request.headers['UserPrincipalName']).first()

            if user is None:
                return "No User", 500

            project = Project.query.filter(func.lower(Project.name) == func.lower(form.data['name'])).first()
            if project is None:
                project = Project()
                project.id = generate_uuid()
                project.name = form.data['name']
                project.url = form.data['url']

                db.session.add(project)
                db.session.commit()

                db.session.refresh(project)

            nomination = Nomination()
            nomination.id = generate_uuid()
            nomination.user_id = user.id
            nomination.project_id = project.id

            return redirect(url_for('nominate.success'))
            

@nominate_blueprint.route('/nominate/success', methods=['GET'])
def success():
    return render_template('nominate_success.html', template='form-template')
