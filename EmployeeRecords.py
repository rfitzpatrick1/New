from logging import debug
from flask import Flask,render_template,request,redirect
import mysql.connector

db = mysql.connector.connect(host="localhost",user="root",password="root",database="business")

cursor=db.cursor()
application=Flask(__name__)

@application.route("/")
def homePage():
    cursor.execute("Select * from consultants")
    data=cursor.fetchall()
    return render_template("Homepage.html",records=data)

@application.route("/editRecord/")
def editrecord(empno):
    cursor.execute("Select * from consultants where empno={0}".format(empno))
    data=cursor.fetchone()
    return render_template("Edit.html",record=data)

@application.route("/filterrecords",methods=["POST"])
def filterrecords():
    if request.form["dept"]=="All":
        return redirect("/")
    else:
        cursor.execute("Select * from consultants where dept='{0}'".format(request.form["dept"]))
        data=cursor.fetchall()
        return render_template("Homepage.html",records=data)

@application.route("/addnewRecord")
def addNewRecord():
    return render_template("Input.html")

@application.route("/saveRecord",methods=["POST"])
def saveRecord():
    cursor.execute("select ifnull(max(regno),0)+1 from consultants");
    newregno=cursor.fetchone()
    name=request.form["na"]
    dept=request.form["dept"]
    salary=request.form["sal"]
    subject=request.form["subject"]
    marks=request.form["marks"]
    sqlquery="insert into consultants values({0},'{1}','{2}','{3}','{4}',{5})".format(newregno[0],name,dept,salary,subject,marks)
    print(sqlquery)
    cursor.execute(sqlquery)
    db.commit()
    return redirect("/")

@application.route("/personaldetails/<empno>")
def personalInformation(empno):
    cursor.execute("Select * from consultants where regno={0}".format(empno))
    data=cursor.fetchone()
    return render_template("record.html",record=data)

@application.route("/deleteEmployee/<empno>")
def deleteEmployee(empno):
    cursor.execute("delete from consultants where regno={0}".format(empno))
    db.commit()
    return redirect("/")

application.run(debug=True)