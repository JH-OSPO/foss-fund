from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length

class CreateNominationForm(FlaskForm):
    name = StringField(
        'Project Name',
        [DataRequired()]
    )

    description = TextAreaField(
        'Description'
    )

    url = StringField(
        'Project URL'
    )

    submit = SubmitField('Submit')
