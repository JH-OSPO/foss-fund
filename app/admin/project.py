from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired

class ProjectForm(FlaskForm):
    name = StringField(
        'Project Name',
        [ DataRequired() ]
    )

    url = URLField(
        'URL'
    )

    description = TextAreaField(
        'Description'
    )

    submit = SubmitField('Submit')


