from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, validators, SubmitField
from wtforms.fields.html5 import DateField


class UserForm(FlaskForm):
   id = HiddenField("Id")

   first_name = StringField("Username: ",[
        validators.DataRequired("Please enter your name."),
   ])

   second_name = StringField("Password: ", [
       validators.DataRequired("Please enter your name."),
   ])

   birthday = DateField("Birthday: ", [
       validators.DataRequired("Please enter your birthday.")])

   city = StringField("City: ",[
       validators.DataRequired("Please enter your city.")
    ])

   submit = SubmitField("Save")