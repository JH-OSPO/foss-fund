from enum import IntEnum, auto
from datetime import datetime,timedelta

from flask import render_template

from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(40), primary_key=True)
    givenname = db.Column(db.String(40))
    surname = db.Column(db.String(40))
    jhed_id = db.Column(db.String(20))
    email = db.Column(db.String(255))
    administrator = db.Column(db.Boolean(name='is_administrator'), default=False, name='is_administrator')
    created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'<Object User id: {self.id} {self.jhed_id}> {self.givenname} {self.surname} ({self.email}) Permissions:{{ self.permissions }}'

    def is_admin(self):
        print(self.administrator)
        return self.administrator
    # def is_permitted(self, item):
    #     return (self.permissions & Permission(item.upper()) == Permission(item.upper()))

class Nomination(db.Model):
    __tablename__= "nominations"
    id = db.Column(db.String(40), primary_key=True)
    user_id = db.Column(db.String(40), db.ForeignKey('users.id'))
    user = db.relationship('User')
    reason = db.Column(db.Text)
    project_id = db.Column(db.String(40), db.ForeignKey('projects.id'))
    nomination_date = db.Column(db.DateTime, default=datetime.now())
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'<Object Nomination id: {self.id}> {self.project.name} (Nominated by: {self.user.jhed_id})'

class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(150))
    url = db.Column(db.String(length=255))
    description = db.Column(db.Text)
    added_by = db.Column(db.String(40), db.ForeignKey('users.id'))
    user = db.relationship('User')
    added_on = db.Column(db.DateTime, default=datetime.now())
    nominations = db.relationship('Nomination', backref="project")
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)

#    def __repr__(self):
#       return f'<Object Project id: {self.id}> {self.name} ({self.url}) (Added by: {self.user.jhed_id})'

    def is_a_candidate(self, campaign_id):
        candidate = CampaignCandidate.query.filter(CampaignCandidate.campaign_id == campaign_id, CampaignCandidate.project_id == self.id).first()
        if candidate is None:
            return False

        return True

class CampaignStatus(IntEnum):
    New = auto()
    Active = auto()
    Abandoned = auto()
    Closed = auto()
    Completed = auto()
    Expired = auto()

class Campaign(db.Model):
    __tablename__ = "campaigns"
    id = db.Column(db.String(40), primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.now())
    length = db.Column(db.Interval)
    created_on = db.Column(db.DateTime, default=datetime.now())
    creator_id = db.Column(db.String(40), db.ForeignKey('users.id'))
    creator = db.relationship('User')
    candidates = db.relationship("CampaignCandidate", back_populates="campaign")
    status_code = db.Column(db.Integer(), default=1)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def __repr__(self):
    #     return f'<Object Campaign id: {self.id}> {self.start_date}-{self.start_date + self.length} created on {self.created_on}'

    @property
    def status(self):
        pass
    
class CampaignCandidate(db.Model):
    __tablename__ = "candidates"
    id = db.Column(db.String(40), primary_key=True)
    
    campaign_id = db.Column(db.String(40), db.ForeignKey('campaigns.id'))
    campaign = db.relationship('Campaign')
    project_id = db.Column(db.String(40), db.ForeignKey('projects.id'))
    project = db.relationship('Project')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'<Object CampaignCandidtate id: {self.id}> Project Name: {self.project.name}, Campaign Name: {self.campaign.name}'

class Vote(db.Model):
    __tablename__ = "votes"

    id = db.Column(db.String(40), primary_key=True)
    campaign_id = db.Column(db.String(40), db.ForeignKey('campaigns.id'))
    campaign = db.relationship('Campaign')
    user_id = db.Column(db.String(40), db.ForeignKey('users.id'))
    user = db.relationship('User')
    votes = db.Column(db.JSON)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

       
