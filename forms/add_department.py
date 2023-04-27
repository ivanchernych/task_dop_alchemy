from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, EmailField
from wtforms.validators import DataRequired


class AddDepartment(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    chief = IntegerField('Chief', validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')
