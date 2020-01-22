from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, validators, SubmitField


class SkillForm(FlaskForm):
   id = HiddenField("Id")

   name = StringField("Programing language: ",[
        validators.DataRequired("Please enter programing language."),
   ])

   submit = SubmitField("Save")