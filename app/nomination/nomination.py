from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.fields.html5 import URLField, SearchField
from wtforms.validators import DataRequired


class UserNominationForm(FlaskForm):
    name = StringField(
        'Project Name',
        [DataRequired()]
    )

    url = URLField(
        'Project URL'
    )

    reason = TextAreaField(
        'How are you using this project?'
    )

    submit = SubmitField('Submit')

    
