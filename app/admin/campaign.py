from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length

class CreateCampaignForm(FlaskForm):
    name = StringField(
        'Campaign Name',
        [DataRequired()]
    )

    startDate = DateField(
        'Start Date',
        format='%Y-%m-%d'
    )

    campaignLength = TextField(
        'Number of Days the campaign will run',
        [
            DataRequired(),
            Length(min=1, max=3)
        ]
    )

    status = SelectField(
        'Status',
        validate_choice = False
    )
    
    submit = SubmitField('Submit')
