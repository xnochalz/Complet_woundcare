from flask import Flask, render_template, redirect, url_for, flash
from flask import Flask, render_template, redirect, url_for, flash, request
from functools import wraps
from flask import abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegisterForm, AddPatient
from wtforms import StringField, SubmitField, PasswordField, SelectField, validators
import os
import smtplib
import sqlite3




OWN_EMAIL = "ngrtnz@gmail.com"
OWN_PASSWORD = "@28+.MAN"

app = Flask(__name__)
app.secret_key = "never say never"
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
gravatar = Gravatar(app, size=100, rating='g', default='intro')


All_patients = []





##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL",  "sqlite:///woundcare.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# login_manager = LoginManager()
# login_manager.init_app(app)


# db = sqlite3.connect("woundcare.db")



# Create the User Table
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    Full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    Gender = db.Column(db.String(100), nullable=False)
    Date_of_birth = db.Column(db.String(100), nullable=False)
    Card_number = db.Column(db.String(100), nullable=False)
    Height = db.Column(db.String(100), nullable=False)
    Medical_History = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)




# # Create all the tables in the database
db.create_all()


# Create the User Table
class CreatePatient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    Clinic_Visit = db.Column(db.String(100), nullable=False)
    tissue_loss = db.Column(db.String(100), nullable=False)
    edges = db.Column(db.String(100), nullable=False)
    exudate_amount = db.Column(db.String(100), nullable=False)
    odor = db.Column(db.String(100), nullable=False)
    peri_wound = db.Column(db.String(100), nullable=False)
    wound_pain = db.Column(db.String(100), nullable=False)
    # wound_color = db.Column(db.String(100), nullable=False)
    wound_integrity = db.Column(db.String(100), nullable=False)
    wound_temperature = db.Column(db.String(100), nullable=False)
    wound_texture = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.String(100), nullable=False)
    bmi = db.Column(db.String(100), nullable=False)
    anatomic_location = db.Column(db.String(100), nullable=False)
    type_of_tissue = db.Column(db.String(100), nullable=False)


# # Create all the tables in the database
db.create_all()

# #CREATE RECORD
# new_wound = User( email="admin@gmail.com", password="123456", username="gee", Cardnumber="0123456", fullname="yes men")
# db.session.add(new_wound)
# db.session.commit()



#Create admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        #Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def home():
    all_users = db.session.query(User).all()
    # wound_patients = CreatePatient.query.all()
    return render_template('index.html', users=all_users)


@app.route('/all')

def all_patients():
    # all_patients = db.session.query(CreatePatient).all()
    wound_patients = CreatePatient.query.all()
    return render_template('all-patients.html', wounds=wound_patients)

@app.route('/users')
# @login_required
def users():
    all_users = db.session.query(User).all()
    # wound_patients = CreatePatient.query.all()
    return render_template('all_users.html', users=all_users)



@app.route('/show-patients')
def show():
    # all_books = session.query(User).all()

    return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def register():

    register_form = RegisterForm()
    if register_form.validate_on_submit():
        if register_form.email.data == "" and register_form.password.data == "":
            return render_template("reports.html")
        else:
            return render_template("login.html")

    return render_template("register2.html", form=register_form)

@app.route("/form-entry", methods=["POST"])
def receive_data():
        if request.method == "POST":
            data = request.form
            print(data["username"])
            print(data["password"])
            print(data["fullname"])
            print(data["dob"])
            print(data["cardnumber"])
            print(data["gender"])
            print(data["height"])
            print(data["history"])
            print(data["fullname"])

            return render_template("register.html", msg_sent=True)

        return render_template("register.html", msg_sent=False)

@app.route('/secrets')
@login_required
def secrets():
    name=(current_user.name)
    return render_template("secrets.html", name=name)



@app.route("/contact", methods=["POST", "GET"])
def contact():
    Add_Patient = AddPatient()
    if Add_Patient.validate_on_submit():
        if Add_Patient.odor.data == "" and Add_Patient.edges.data == "":
            return render_template("reports.html")
        else:
            return render_template("login.html")
        return render_template('login.html', form=AddPatient)

    return render_template("reports.html", form=Add_Patient)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Find user by email entered.
        user = User.query.filter_by(email=email).first()

        # Check stored password hash against entered password hashed.
        if check_password_hash(user.password, password):
            login_user(user)

            # login_form = LoginForm()
            # if login_form.validate_on_submit():
            #     if login_form.email.data == "admin@email.com" and login_form.password.data == "12345678":
            #         return render_template("reports.html")
            #     else:
            return redirect(url_for('secrets'))
    return render_template('login.html', form=login_form)


@app.route("/register-user", methods=["POST", "GET"])
def register_data():
        if request.method == "POST":
            hash_and_salted_password = generate_password_hash(
                request.form.get('password'),
                method='pbkdf2:sha256',
                salt_length=8
            )
            # CREATE RECORD
            new_user = User(
                Full_name=request.form["fullname"],

                username=request.form["username"],
                email=request.form["email"],
                Gender=request.form["gender"],
                Date_of_birth=request.form["dob"],
                Height=request.form["height"],
                Medical_History=request.form["history"],
                Card_number=request.form["cardnumber"],
                password=hash_and_salted_password

            )
            db.session.add(new_user)
            db.session.commit()

            # Log in and authenticate user after adding details to database.
            login_user(new_user)

            return redirect(url_for('users'))

        return render_template("register.html")

@app.route("/add", methods=["GET", "POST"])
# @login_required
def add_patient():
    if request.method == "POST":

        # CREATE RECORD
        new_patient = CreatePatient(
            odor=request.form["odor"],
            weight=request.form["weight"],
            tissue_loss=request.form["tissueloss"],
            edges=request.form["edges"],
            exudate_amount=request.form["exudate"],
            peri_wound=request.form["periwound"],
            wound_integrity=request.form["woundintegrity"],
            wound_temperature=request.form["woundtemperature"],
            wound_texture=request.form["woundtexture"],
            wound_pain=request.form["woundpain"],
            bmi=request.form["bmi"],
            anatomic_location=request.form["anatomiclocation"],
            type_of_tissue=request.form["bmi"],
            Clinic_Visit=request.form["clinicvisit"]
        )
        db.session.add(new_patient)
        db.session.commit()

        return redirect(url_for('all_patients'))

    return render_template("create_patient.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # UPDATE RECORD
        patient_id = request.form["id"]
        patient_to_update = CreatePatient.query.get(patient_id)
        patient_to_update.tissue_loss = request.form["tissueloss"]
        db.session.commit()
        return redirect(url_for('all'))
    patient_id = request.args.get('id')
    patient_selected = CreatePatient.query.get(patient_id)
    return render_template("edit_patient.html", patients=patient_selected)



@app.route("/delete")
def delete():
    patient_id = request.args.get('id')
    # DELETE A RECORD BY ID
    patient_to_delete = CreatePatient.query.get(patient_id)
    db.session.delete(patient_to_delete)
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)