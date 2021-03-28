from flask_wtf import FlaskForm
from wtforms import SubmitField

class VoteForm(FlaskForm):
    submit = SubmitField('submit')
