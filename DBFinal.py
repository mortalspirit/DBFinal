from flask import Flask, g, render_template, url_for, request
import sqlite3
import pymysql
import datetime
from datetime import datetime

conn = pymysql.connect(host="us-cdbr-iron-east-05.cleardb.net", user="b07f9bd28a1df0", password="68ccaea4",
                        database="heroku_bafe54ca91a5de3")
cursor = conn.cursor()


app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')



@app.route('/about')
def about():
    sql = 'select * FROM Student'
    cur = cursor.execute(sql)
    students = [dict(StudentMUNumber=row[0], StaffNumber=row[1], StudentFirstName=row[2], StudentLastName=row[3]) for row in cursor.fetchall()]
    return render_template('about.html', students=students)
@app.route('/diagram')
def diagram():
    return render_template('diagram.html')

@app.route('/queries')
def queries():
    return render_template('queries.html')
@app.route('/query_post', methods=['GET', 'POST'])
def query_post():
    querynum = request.form.get('querycontroller')
    print(querynum)
    object = None
    if querynum == "1":
        sql = 'SELECT ResidenceHallName, ResidenceHallManager, ResidenceHallPhone FROM residencehall'
        cur = cursor.execute(sql)
        object = [dict(ResidenceHallName=row[0], ResidenceHallManager=row[1], ResidenceHallPhone=row[2])
                    for row in cursor.fetchall()]
    if querynum == "2":
        sql = 'SELECT student.StudentMUNumber, student.StudentFirstname, student.StudentLastName, lease.LeaseDuration, lease.DateEntered, lease.DateLeave, lease.Semester FROM Student INNER JOIN lease ON student.StudentMUNumber=lease.StudentMUNumber  ;'
        cur = cursor.execute(sql)
        object = [dict(StudentMUNumber=row[0], StudentFirstName=row[1], StudentLastName=row[2], LeaseDuration=row[3].strftime("%B %d, %Y"), LeaseDateEntered=row[4].strftime("%B %d, %Y"), LeaseDateLeave=row[5], Semester=row[6])
                  for row in cursor.fetchall()]
    if querynum == "3":
        sql = 'SELECT * FROM Lease WHERE Semester = "Summer";'
        cur = cursor.execute(sql)
        object = [dict(LeaseNumber=row[0], StudentMUNumber=row[1], PlaceNumber=row[2], LeaseDuration=row[3].strftime("%B %d, %Y"),
                       LeaseDateEntered=row[4].strftime("%B %d, %Y"), LeaseDateLeave=row[5], Semester=row[6])
                  for row in cursor.fetchall()]

    if querynum == "4":
        sql = 'SELECT SUM(InvoiceAmount), lease.LeaseNumber, lease.StudentMUNumber FROM invoice INNER JOIN lease ON invoice.LeaseNumber=lease.LeaseNumber WHERE lease.StudentMUNumber = "1"'

        cur = cursor.execute(sql)
        object = [dict(SUM=row[0], LeaseNumber=row[1], StudentMUNumber = row[2])
                  for row in cursor.fetchall()]
    if querynum == "5":

        sql = 'SELECT student.StudentFirstName, student.StudentLastName, invoice.InvoicePaid, invoice.InvoicePaymentDue FROM student INNER JOIN lease on student.StudentMUNumber=lease.studentMUNumber INNER JOIN invoice ON invoice.LeaseNumber=lease.LeaseNumber WHERE invoice.InvoicePaid = "0" AND invoice.InvoicePaymentDue <= "2019-04-22 21:40:18.351" '
        cur = cursor.execute(sql)
        object = [dict(StudentFirstName=row[0], StudentLastName=row[1], InvoicePaid=row[2], InvoicePaymentDue=row[3])
                  for row in cursor.fetchall()]
    if querynum == "6":
        sql = 'SELECT InspectionNumber, ApartmentNumber, StaffNumber, InspectionInspectionGood, InspectionDate, InspectionComments FROM studentapartmentinspections WHERE InspectionInspectioNGood ="0"'

        cur = cursor.execute(sql)
        object = [dict(InspectionNumber=row[0], ApartmentNumber=row[1], StaffNumber=row[2], InspectionInspectionGood=row[3], InspectionDate=row[4], InspectionComments=row[5])
                  for row in cursor.fetchall()]
    if querynum == "7":

        sql = 'SELECT student.StudentMUNumber, student.StudentFirstName, student.StudentLastName, room.PlaceNumber, room.RoomNumber FROM student INNER JOIN lease on student.StudentMUNumber=lease.studentMUNumber INNER JOIN room ON lease.PlaceNumber=room.PlaceNumber WHERE room.ResidenceHallNumber = "1" '
        cur = cursor.execute(sql)
        object = [dict(StudentMUNumber=row[0], StudentFirstName=row[1], StudentLastName=row[2], PlaceNumber=row[3], RoomNumber=row[4])
                  for row in cursor.fetchall()]
    if querynum == "8":
        sql = 'SELECT StudentMUNumber, StudentFirstName, StudentLastName, StudentEmail, StudentCategory FROM student WHERE StudentStatus = "0"'

        cur = cursor.execute(sql)
        object = [dict(StudentMUNumber=row[0], StudentFirstName=row[1], StudentLastName=row[2], StudentEmail=row[3],
                       StudentCategory=row[4])
                  for row in cursor.fetchall()]
    if querynum == "9":
        sql = 'SELECT StudentMUNumber, StudentFirstName, StudentLastName, StudentEmail, StudentCategory FROM student WHERE StudentStatus = "0"'

        cur = cursor.execute(sql)
        object = [dict(StudentMUNumber=row[0], StudentFirstName=row[1], StudentLastName=row[2], StudentEmail=row[3],
                       StudentCategory=row[4])
                  for row in cursor.fetchall()]

    return render_template('query_post.html', object=object, querynum=querynum)


if __name__ == '__main__':
    app.run()



