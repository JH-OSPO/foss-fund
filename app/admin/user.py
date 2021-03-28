from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, HiddenField, BooleanField
from wtforms.validators import DataRequired, Length

class CreateUserForm(FlaskForm):
    jhed_id = TextField(
        'JHED ID',
        [
            DataRequired(),
            Length(max=8, min=3)
        ]
    )

    submit = SubmitField('Submit')

class UpdateUserForm(FlaskForm):
    is_admin = BooleanField(
        "Administrator"
    )

