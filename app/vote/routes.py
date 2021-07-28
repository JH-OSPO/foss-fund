from flask import Blueprint, request, abort, render_template, jsonify, make_response, redirect, url_for
from flask_sqlalchemy import get_debug_queries
from app.models import *
from app import is_development, generate_uuid
from .vote import VoteForm
import json
from sqlalchemy import desc, and_
import datetime


from enum import IntFlag, auto

vote_blueprint = Blueprint('vote_blueprint', __name__)

@vote_blueprint.route('/vote', methods=['GET'])
@vote_blueprint.route('/vote/latest', methods=['GET'])
def vote_default():
    mydatetime = datetime.datetime.now()
    print("%s:%s" %(mydatetime, CampaignStatus.Active.value))
    campaign = Campaign.query.filter( and_ ( 
               Campaign.status_code == CampaignStatus.Active.value,
               Campaign.end_date > mydatetime,
               Campaign.start_date < mydatetime)).order_by(desc('start_date')).first()
    if campaign is not None:
        print(campaign.start_date + campaign.length)
        return(redirect(url_for('vote_blueprint.vote', campaign_id = campaign.id)))
    else:
        return(render_template('no-vote.html'))

@vote_blueprint.route('/vote/<campaign_id>', methods=['GET', 'POST'])
def vote(campaign_id = None):
    if campaign_id is None:
        return "test"

    if is_development():
        print("In development")
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
        print(request.form)
        data = request.form
        print (data.get('jhed_id'))
        user = User.query.filter(User.jhed_id == data.get('jhed_id')).first()
        print(user)
        if user is None:
            abort(500)
            
        vote = Vote.query.filter(Vote.user_id == user.id, Vote.campaign_id == campaign_id).first()
        if vote is not None:
            return(render_template('vote_done.html', campaign=campaign, candidates=campaign.candidates, user=user, form=form))

        vote = Vote()
        vote.id = generate_uuid()
        vote.campaign_id = campaign_id
        vote.user_id = user.id
        print(data.get('votes'))
        print(json.dumps(data.get('votes')))
        vote.votes = data.get('votes')
        vote.date = datetime.datetime.now()
        db.session.add(vote)
        db.session.commit()

        return redirect(url_for('vote_blueprint.vote', campaign_id=campaign_id))

    
    return(render_template('vote_form.html', campaign=campaign, candidates=campaign.candidates, user=user, form=form))
