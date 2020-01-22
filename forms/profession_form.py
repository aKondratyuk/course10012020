from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, validators, SubmitField
from wtforms.fields.html5 import IntegerField


class ProfessionForm(FlaskForm):
   id = HiddenField("Id")

   name = StringField("Image URL: ",[
        validators.DataRequired("Please enter url"),
   ])

   minimal_work_expirience = IntegerField("Size: ",
        [validators.DataRequired("Minimal work expirience required"), validators.NumberRange(min=1, max=5)]
    )

   minimal_education = StringField("Format of Image: ", [
       validators.DataRequired("Please enter your birthday."),
       validators.length(4, 60, "Pleas select between 4 to 60")
   ])

   category = StringField("Topic: ",[
       validators.DataRequired("Please enter topic."),
       validators.length(10, 100, "Pleas select between 10 to 100")
    ])

   submit = SubmitField("Save")