from flask import Blueprint, request, render_template, redirect, url_for, current_app, session, jsonify, flash, abort
from app.models import User, Campaign, Nomination, CampaignCandidate, Project, CampaignStatus, Vote
from sqlalchemy import func, desc
from . import admin_blueprint
from .campaign import CreateCampaignForm

import datetime
import jsonpickle
import json

from app import db, generate_uuid, is_development
import datetime


permission = "admin_campaigns"

@admin_blueprint.route('/admin/campaign', methods=['GET', 'POST'])
def list_campaigns():
    if request.method == 'GET':
        current_app.jinja_env.filters['timedelta'] = datetime.timedelta
        return render_template('list_campaigns.html', campaigns=Campaign.query.all())
    else:
        form = CreateCampaignForm()

@admin_blueprint.route('/admin/campaign/add', methods=['GET', 'POST'])
def create_campaign():
    flash('This is a test', 'success')
    form = CreateCampaignForm()
    if request.method == "GET":
        if form.validate_on_submit():
            return redirect('https://www.google.com')
        return render_template(
            "create_campaign_form.html",
            form = form,
            template="form-template"
        )
    else:
        if form.validate_on_submit():
            if is_development():
                u = User.query.filter(User.jhed_id == 'dbelros1').first()
            else:
                u = User.query.filter(User.jhed_id == request.headers.get('Userprincipalname')).first()
                
            f = form.data
            print(f)
            c = Campaign()
            c.id = generate_uuid()
            c.title = f.get('name')
            c.start_date = f.get('startDate')
            c.length = datetime.timedelta(days=int(f.get('campaignLength')))
            c.creator_id = u.id
            print(c)
            
            db.session.add(c)
            db.session.commit()

        else:
            print(f)
        return redirect(url_for('admin_blueprint.list_campaigns'))
    
@admin_blueprint.route('/admin/campaign/<campaign_id>', methods=['GET', 'POST'])
def campaign_view(campaign_id):
    form = CreateCampaignForm()
    if request.method == 'GET':
        c = Campaign.query.filter(Campaign.id == campaign_id).first()
        statuses = CampaignStatus
        candidates = CampaignCandidate.query.filter(CampaignCandidate.campaign_id == c.id)
        projects_list = Project.query.join(Nomination, Project.id == Nomination.project_id).add_column(func.count(Nomination.project_id).label("nomination_count")).group_by(Nomination.project_id).order_by(desc('nomination_count'))
        print(projects_list)
        projects = []
        statuses = []

        for status in CampaignStatus:
            statuses.append((status.value, status.name))
        
        for project,count in projects_list:
            projects.append(project)
            print(f"{project.name} {len(project.nominations)}")

        form.status.choices = statuses
        form.status.process_data(c.status_code)
                
        return render_template('campaign_details.html', campaign=c, form=form, projects=projects, candidates=candidates, statuses=statuses)
    elif request.method == 'POST':
        if form.validate_on_submit():
            c = Campaign.query.filter(Campaign.id == campaign_id).first()

            f = form.data
            if c is None:
                abort(500)
            else:
                c.title = f['name']
                c.date = f['startDate']
                c.length = datetime.timedelta(days=int(f['campaignLength']))
                c.status_code = f['status']
                print(c)
                db.session.commit()
                
                return jsonify(title=c.title, start_date = c.start_date, length=c.length.days, new_end_date=(c.start_date + c.length).strftime('%B %d, %Y'), status=c.status_code)

        print(form.errors)
        return "oops", 500
    
@admin_blueprint.route('/admin/campaign/<campaign_id>/add_candidate', methods=['POST'])
def add_campaign_candidate(campaign_id):
    if request.method == "POST":
        data = request.get_json()
        project = Project.query.filter(Project.id == data['project_id']).first()
        campaign = Campaign.query.filter(Campaign.id == campaign_id).first()
        if project is None or campaign is None:
            abort(500)
        else:
            candidate = CampaignCandidate()
            candidate.id = generate_uuid()
            candidate.campaign_id = campaign.id
            candidate.project_id = project.id
            db.session.add(candidate)
            db.session.commit()

        print(f"{campaign_id} has been assigned {candidate.id}")
        return candidate.id
        

@admin_blueprint.route('/admin/campaign/<campaign_id>/remove_candidate', methods=['POST'])
def remove_campaign_candidate(campaign_id):
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        candidate = CampaignCandidate.query.filter(CampaignCandidate.id == data['candidate_id']).first()
        if candidate is None:
            abort(404)
        else:
            db.session.delete(candidate)
            db.session.commit()

        return {'project_id': candidate.project_id}

@admin_blueprint.route('/admin/campaign/<campaign_id>/results', methods=['GET'])
def campaign_results(campaign_id):
    if campaign_id is None:
        return abort(500)
    
    votes = []
    v = Vote.query.filter(Vote.campaign_id == campaign_id)

    for voteobj in v:
        vote ={}
        vote['id'] = voteobj.id
        vote['user'] = json.loads(voteobj.user.toJson())
        vote['votes'] = []
        print(f" Test: {json.loads(voteobj.votes)}")
        for candidate_id in json.loads(voteobj.votes)['votes']:
           candidate = CampaignCandidate.query.filter(CampaignCandidate.id == candidate_id).first()
           vote['votes'].append(json.loads(candidate.toJson()))
        
        votes.append(vote)
    
    return jsonify(votes)

@admin_blueprint.route('/admin/campaign/<campaign_id>/candidates', methods = ['GET'])
def campaign_candidates(campaign_id):
    if campaign_id is None:
        return abort(500)
    
    campaign = Campaign.query.filter(Campaign.id == campaign_id).first()
    candidates = []
    for candidate in campaign.candidates:
        candidates.append(json.loads(candidate.toJson()))

    return jsonify(candidates)