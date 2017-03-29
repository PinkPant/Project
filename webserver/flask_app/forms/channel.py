from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField
from wtforms.validators import DataRequired

__all__ = ["CreateForm", "DeleteForm"]


class CreateForm(FlaskForm):
    name = StringField("Name", [DataRequired()])


class DeleteForm(FlaskForm):
    name = HiddenField("Name", [DataRequired()])
