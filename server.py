import mysql.connector
from flask import Flask, redirect, url_for, request,render_template

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql",
  database="MyPythonDatabase"
)
mycursor = mydb.cursor()
app = Flask(__name__)

@app.route('/')
def hello_world():
   return render_template("index.html")

@app.route('/addDoctor', methods=['GET','POST'])
def add():
    if request.method == 'POST': 
        name = request.form['DoctorName']
        dep = request.form['DoctorDepartment']
        id = request.form['DoctorID']
        sql="INSERT INTO Doctors (name,department,id) VALUES (%s,%s,%s)"
        values=(name,dep,id)
        mycursor.execute(sql,values)
        mydb.commit()
        return render_template("index.html")
    else:
        return render_template("addDoctor.html")

@app.route('/viewDoctor')
def view():
    mycursor.execute("SELECT * FROM Doctors")
    row_headers=[x[0] for x in mycursor.description]
    myresult = mycursor.fetchall()
    return render_template("viewDoctor.html",DoctorsData=myresult)

if __name__ == '__main__':
   app.run()