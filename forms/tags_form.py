from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, validators, SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import IntegerField


class VacancyForm(FlaskForm):
    id = HiddenField("Id")

    name = StringField("Tag name: ",[
        validators.DataRequired("Please enter name."),
    ])

    duties = StringField("Duties: ",[
        validators.DataRequired("Please enter duties."),
    ])

    salary = IntegerField("User Trafic: ", [
        validators.DataRequired("User Trafic is required")
    ])

    description = StringField("Description: ", [
        validators.DataRequired("Please enter description."),
    ])

    profession_id = SelectField("Image: ", choices=[], coerce=int)  # ,[validators.DataRequired(),])

submit = SubmitField("Save")