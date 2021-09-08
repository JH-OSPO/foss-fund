# from flask import BluePrint, request, abort
# from app.models import *

# from enum import IntFlag, auto

# class CampaignStatus(IntFlag):
#     New = auto()
#     Active = auto()
#     Abandoned = auto()
#     Closed = auto()
#     Completed = auto()
#     Expired = auto()

# vote_blueprint = BluePrint('vote', __name__)

# @nominate_blueprint.route('/vote/latest', methods=["GET","POST"])
# def latest_vote():

# @nominate_blueprint.route('/vote/<campaign_id>', methods=['GET', 'POST'])
# def vote(campaign_id):
#     if request.method == 'GET':
#         campaign = Campaign.query.filter(Campaign.id == campaign_id)
#         if campaign is None:
#             abort(500)
            
#     elif request.method == 'POST':
        
#     return(campaign.candidates)
            
