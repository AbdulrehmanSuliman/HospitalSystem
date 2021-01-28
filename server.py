import mysql.connector
from flask import Flask, redirect, url_for, request,render_template, session, flash
from functools import wraps

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
app = Flask(__name__)
app.secret_key = 'aS2X7Ku9=&LEaRu7'
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



@app.route('/viewDoctor')
@login_required
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