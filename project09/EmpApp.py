from flask import Flask, render_template, request
from pymysql import *
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'empdata'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('AddEmp.html')

def insert_details(ename,email, ephno, exp, apt,gdscore,hrscore,location):
    cur=db_conn.cursor()
    cur.execute("INSERT INTO empdata(ename,email, ephno, exp, apt,gdscore,hrscore,location) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (ename,email, ephno, exp, apt,gdscore,hrscore,location))
    db_conn.commit()#read the data

def get_details():
    cur=db_conn.cursor()
    cur.execute("SELECT *  FROM empdata")
    empdata = cur.fetchall()
    return empdata

@app.route('/insert',methods = ['post'])
def insert():
    
    if request.method == 'POST':
        ename = request.form['ename']
        email = request.form['email']
        ephno = request.form['ephno']
        exp = request.form['exp']
        apt = request.form['apt']
        gdscore = request.form['gdscore']
        hrscore = request.form['hrscore']
        location = request.form['location']
        insert_details(ename,email, ephno, exp, apt,gdscore,hrscore,location)
        empdata = get_details()
        print(empdata)
        for detail in empdata:
            var = detail
        return render_template('AddEmp.html',var=var)


@app.route("/about", methods=['POST'])
def about():
    return render_template('#')

@app.route("/addemp", methods=['POST'])
def AddEmp():
    ename = request.form['ename']
    email = request.form['email']
    ephno = request.form['ephno']
    exp = request.form['exp']
    apt = request.form['apt']
    gdscore = request.form['gdscore']
    hrscore = request.form['hrscore']
    location = request.form['location']
    emp_resume = request.files['emp_resume']

    insert_sql = "INSERT INTO empdata VALUES (%s, %s, %s, %s, %s ,%s ,%s ,%s)"
    cursor = db_conn.cursor()
    if emp_resume.filename == "":
        return "Please select a file"

    try:

        cursor.execute(insert_sql, (ename,email, ephno, exp, apt,gdscore,hrscore,location))
        db_conn.commit()
        # Uplaod image file in S3 #
        emp_resume_name_in_s3 = "emp-name-" + str(ename) + "_Resume"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=emp_resume_name_in_s3, Body=emp_resume)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                emp_resume_name_in_s3)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('AddEmpOutput.html', name=ename,email=email,phno=ephno,experience=exp,aptitude=apt,gd=gdscore,hr=hrscore,loc=location)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
