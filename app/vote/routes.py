from flask import Blueprint, request, abort, render_template, jsonify, make_response, redirect, url_for
from app.models import *
from app import is_development, generate_uuid
from .vote import VoteForm
import json
from sqlalchemy import desc


from enum import IntFlag, auto

vote_blueprint = Blueprint('vote_blueprint', __name__)

@vote_blueprint.route('/vote', methods=['GET'])
@vote_blueprint.route('/vote/latest', methods=['GET'])
def vote_default():
    print(CampaignStatus.Active)
    campaign = Campaign.query.filter(Campaign.status_code == CampaignStatus.Active.value).order_by(desc('start_date')).first()
    return(redirect(url_for('vote_blueprint.vote', campaign_id = campaign.id)))
    

@vote_blueprint.route('/vote/<campaign_id>', methods=['GET', 'POST'])
def vote(campaign_id = None):
    if campaign_id is None:
        return "test"

    if is_development():
        user = User.query.filter(User.jhed_id == 'dbelros1').first()
    else:
        user = User.query.filter(User.jhed_id == request.headers['UserPrincipalName']).first()

    if user is None:
        abort(500)

    campaign = Campaign.query.filter(Campaign.id == campaign_id).first()
    if campaign is None:
        abort(500)
        
    form = VoteForm()
    
    if request.method == 'GET':
        print(campaign_id)
        print(user.jhed_id)
        v = Vote.query.filter(Vote.user_id == user.id, Vote.campaign_id == campaign_id).first()
        if v is not None:
            return(render_template('vote_done.html', campaign=campaign, candidates=campaign.candidates, user=user, form=form))
        else:
            print("vote does not exist")
    elif request.method == 'POST':
        data = request.get_json()
        user = User.query.filter(User.jhed_id == data['jhed_id']).first()
        if user is None:
            abort(500)
            
        vote = Vote.query.filter(Vote.user_id == user.id, Vote.campaign_id == campaign_id).first()
        if vote is not None:
            return(render_template('vote_done.html', campaign=campaign, candidates=campaign.candidates, user=user, form=form))

        vote = Vote()
        vote.id = generate_uuid()
        vote.campaign_id = campaign_id
        vote.user_id = user.id
        vote.votes = json.dumps(data['votes'])
        db.session.add(vote)
        db.session.commit()

        return "Done", 200

    
    return(render_template('vote_form.html', campaign=campaign, candidates=campaign.candidates, user=user, form=form))