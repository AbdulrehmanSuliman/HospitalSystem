import mysql.connector
from flask import Flask, redirect, url_for, request,render_template, session, flash
from functools import wraps
from flask_mail import Message, Mail
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, TextField
from wtforms import ValidationError, validators


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql",
  database="MyPythonDatabase"
)
mycursor = mydb.cursor()
#mycursor.execute("CREATE TABLE Doctors (name VARCHAR(255),department VARCHAR(255), id INT, PRIMARY KEY(id))")
#mycursor.execute("CREATE TABLE Patients (name VARCHAR(255), id INT, PRIMARY KEY(id))")
#mycursor.execute("CREATE TABLE ROOM ( RoomID INT,time VARCHAR(255), D_code INT, P_code INT, PRIMARY KEY(RoomID), FOREIGN KEY (P_code) REFERENCES Patients(id),FOREIGN KEY (D_code) REFERENCES Doctors(id))")
#mycursor.execute("CREATE TABLE Requests (name VARCHAR(255), id INT,email VARCHAR(255),dname VARCHAR(255), PRIMARY KEY(id))")
app = Flask(__name__)
app.secret_key = 'aS2X7Ku9=&LEaRu7'
app.config['SECRET_KEY'] = "mysecretkeywhichissupposedtobesecret"
app.config['MAIL_SERVER'] = "smtp-mail.outlook.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "abd2000_mah@hotmail.com"
app.config['MAIL_PASSWORD'] = "332211"
mail = Mail(app)
@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        msg = Message(
            subject=f"Mail from {name}", body=f"Name: {name}\nE-Mail: {email}\nPhone: {phone}\n\n\n{message}", sender='[SENDER EMAIL]', recipients=['Hisapp12@hotmail.com'])
        mail.send(msg)
        return render_template("contact.html", success=True)

    return render_template("contact.html")

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
@app.route('/')
@login_required
def home():
   return render_template("index.html")
@app.route('/PatientPage')
def Pat():
   return render_template("Patient.html")


@app.route('/addRequest', methods=['GET','POST'])
def addR():
    if request.method == 'POST': 
        name = request.form['PatientName']
        id = request.form['PatientID']
        email = request.form['Email']
        dname=request.form['dName']
        try:
            sql="INSERT INTO Requests (name,id,email,dname) VALUES (%s,%s,%s,%s)"
            values=(name,id,email,dname)
            mycursor.execute(sql,values)
            mydb.commit()
            return render_template("Request.html", succ="Request Registered.")
        except:
            return render_template("Request.html", err="Something wrong in the inputs.")
    else:
        return render_template("Request.html")



@app.route('/addDoctor', methods=['GET','POST'])
@login_required
def add():
    if request.method == 'POST': 
        name = request.form['DoctorName']
        dep = request.form['DoctorDepartment']
        id = request.form['DoctorID']
        try:
            sql="INSERT INTO Doctors (name,department,id) VALUES (%s,%s,%s)"
            values=(name,dep,id)
            mycursor.execute(sql,values)
            mydb.commit()
            return render_template("addDoctor.html", succ="Doctor Registered.")
        except:
            return render_template("addDoctor.html", err="Something wrong in the inputs.")
    else:
        return render_template("addDoctor.html")

@app.route('/viewRequests')
@login_required
def viewR():
    mycursor.execute("SELECT * FROM Requests")
    row_headers=[x[0] for x in mycursor.description]
    myresult = mycursor.fetchall()
    return render_template("viewRequests.html",RequestsData=myresult)


@app.route('/viewDoctor')
def view():
    mycursor.execute("SELECT * FROM Doctors")
    row_headers=[x[0] for x in mycursor.description]
    myresult = mycursor.fetchall()
    return render_template("viewDoctor.html",DoctorsData=myresult)

@app.route('/viewPatients')
@login_required
def viewP():
    mycursor.execute("SELECT * FROM Patients")
    row_headers=[x[0] for x in mycursor.description]
    myresult = mycursor.fetchall()
    return render_template("viewPatients.html",DoctorsData=myresult)

@app.route('/viewAppointments')
@login_required
def viewA():
    mycursor.execute("SELECT * FROM Room")
    row_headers=[x[0] for x in mycursor.description]
    myresult = mycursor.fetchall()
    return render_template("viewAppointments.html",DoctorsData=myresult)


@app.route('/addPatient', methods=['GET','POST'])
@login_required
def addP():
    if request.method == 'POST': 
        name = request.form['PatientName']
        id = request.form['PatientID']
        Docid=request.form['DocID']
        room= request.form['RoomID']
        time=request.form['Time']
        try:
            sql="INSERT INTO Patients (name,id) VALUES (%s,%s)"
            values=(name,id)
            mycursor.execute(sql,values)
            mydb.commit()
            sql = "INSERT INTO Room (RoomID,Time, D_code, P_code) VALUES (%s,%s,%s,%s)"
            val = (room,time,Docid,id)
            mycursor.execute(sql, val)
            mydb.commit()
            return render_template("addPatient.html", succ="Patient Registered.")
        except:
            return render_template("addPatient.html", err="Something wrong in the inputs.")
    else:
        return render_template("addPatient.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
   app.run()