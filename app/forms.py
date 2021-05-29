from typing import Optional
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, Length, Optional
from wtforms.fields.html5 import DateTimeLocalField


class TaskForm(FlaskForm):
    task = TextAreaField('Task', validators=[DataRequired(), Length(min=1, max=140)])
    deadline = DateTimeLocalField('Deadline',  format='%Y-%m-%dT%H:%M', validators=[Optional()])
    submit = SubmitField('Submit')


class CompletedForm(FlaskForm):
    complete = SubmitField('')


class DeleteForm(FlaskForm):
    delete = SubmitField('x')
