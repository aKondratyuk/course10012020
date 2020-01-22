from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField, SelectField


class UserSkillForm(FlaskForm):
   id = HiddenField("Id")

   skill_id = SelectField("Programing language: ", choices=[], coerce=int)#,[validators.DataRequired(),])

   user_id = SelectField("Username: ", choices=[], coerce=int)#,[validators.DataRequired(),])

   submit = SubmitField("Save")