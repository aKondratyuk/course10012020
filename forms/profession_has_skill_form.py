from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField, SelectField


class ProfessionSkillForm(FlaskForm):
   id = HiddenField("Id")

   skill_id = SelectField("Programing language: ", choices=[], coerce=int)#,[validators.DataRequired(),])

   profession_id = SelectField("Image URL: ", choices=[], coerce=int)#,[validators.DataRequired(),])

   submit = SubmitField("Save")