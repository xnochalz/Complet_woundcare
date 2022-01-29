from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, DateField, FloatField, IntegerField, SelectMultipleField, FileField, TextAreaField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField




class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me In!")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    Gender = StringField("Gender", validators=[DataRequired()])
    Date_of_birth = DateField("Date Of Birth", validators=[DataRequired()])
    Card_number = IntegerField("Card Number", validators=[DataRequired()])
    Full_name = StringField("Full Name", validators=[DataRequired()])
    Height = FloatField("Height", validators=[DataRequired()])
    Medical_History = FloatField("Past Medical History", validators=[DataRequired()])
    submit = SubmitField("Register Me!")
    # submit = SubmitField("Sign Me Up!")

class AddPatient(FlaskForm):
    odor = SelectField("Odor", choices=["Absent", "Faint" "Moderate", "Strong", "Purulent", "Foul"], validators=[DataRequired()])
    tissue_loss = SelectMultipleField("Extent of tissue loss (Select All tha Apply)", choices=["Superficial", "Abrasion" "Partial Thickness", "Full thickness", "Necrosis covering wound bed; unable to see dept", "Deep crater", "Tendon, muscle, or bone visible"], validators=[DataRequired()])
    edges = SelectField("Edges", choices=["Attached or open, even with wound base", "Not attached or closed " "Rolled under, thickened", "Fibrotic, scarred "], validators=[DataRequired()])
    exudate_amount = SelectField("Exudate Amount", choices=["Select", "None", "Light" "Moderate", "Heavy"], validators=[DataRequired()])
    peri_wound = SelectField("Peri_wound Color", choices=["Select", "None", "Light" "Moderate", "Heavy"], validators=[DataRequired()])
    wound_integrity = SelectField("Peri wound Integrity",  choices=["Select", "Maceration", "Excoriation" "Erosion", "Edema present"], validators=[DataRequired()] )
    wound_temperature = SelectField("Peri wound Temperature", choices=["Select", "Warm", "Cold"], validators=[DataRequired()])
    wound_texture = SelectField("Peri wound texture", choices=["Select", "Moist", "Dry" "Boggy", "Macerated"], validators=[DataRequired()])
    wound_pain = SelectField("Wound Pain", choices=["Select", "No pain", "moderate pain", "Severe pains"], validators=[DataRequired()])
    edges = SelectField("Edges", choices=["Select", "Attached or open, even with wound base", "Not attached or closed", "Rolled under, thickened", "Fibrotic, scarred"], validators=[DataRequired()])
    weight = StringField("Weight", validators=[DataRequired()])
    bmi = IntegerField("BMI", validators=[DataRequired()])
    anatomic_location = StringField("Anatomic Location", validators=[DataRequired()])
    type_of_tissue = SelectMultipleField("Type of Tissue in wound bed", validators=[DataRequired()])
    # wound = FileField("Wound View")
    submit = SubmitField("Register Patient!")


class EditPatient(FlaskForm):
    weight = StringField("Your Rating Out of 10 e.g. 7.5")
    bmi = StringField("Your Review")
    submit = SubmitField("Done")
