from flask import Flask,render_template,request,redirect
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def hello_world():
   return "Hello World"
@app.route('/students/')
def index():
   con = sql.connect("collegemanagement.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   studentrecord={}
   if 'admn' in request.args:
         print(request.args.get('admn'))
         cur.execute("SELECT * FROM STUDENTSMASTER WHERE ADMISSIONNUMBER = '{}'".format(request.args.get('admn')))
         studentrecord = cur.fetchone()
   cur.execute("select S.ADMISSIONYEAR,S.ADMISSIONNUMBER,S.NAME,S.ADDRESS,S.MOBILE,S.COURSE,D.NAME AS DEPARTMENTNAME\
       from STUDENTSMASTER S,DEPARTMENTMASTER D WHERE D.DEPARTMENTCODE=S.DEPARTMENTCODE ")
   
   rows = cur.fetchall(); 
   cur.execute("select * from departmentmaster")
   
   departments = cur.fetchall(); 
   #return render_template("list.html",rows = rows)
   return render_template("students.html",rows = rows,departments = departments,studentrecord=studentrecord )


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         str_admissionyear = request.form['admissionyear']
         str_admissionnumber = request.form['admissionnumber']
         str_name = request.form['name']
         str_address = request.form['address']
         str_mobile = request.form['mobile']
         str_course = request.form['course']
         str_department = request.form['department']
         with sql.connect("collegemanagement.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO STUDENTSMASTER  (admissionnumber,AdmissionYear,Name,ADDRESS,MOBILE,COURSE,DEPARTMENTCODE)   \
                VALUES (?,?,?,?,?,?,?)",(str_admissionnumber,str_admissionyear,str_name,str_address,str_mobile,str_course,str_department) )
            
            con.commit()
            msg = "Record successfully added"

      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return redirect("/students/?msg="+msg)
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/updatestudent',methods = ['POST', 'GET'])
def updaterecord():
   if request.method == 'POST':
      try:
         str_admissionyear = request.form['admissionyear']
         str_admissionnumber = request.form['admissionnumber']
         str_name = request.form['name']
         str_address = request.form['address']
         str_mobile = request.form['mobile']
         str_course = request.form['course']
         str_department = request.form['department']
         str_studentadm=request.form['updaterecord']
         with sql.connect("collegemanagement.db") as con:
            cur = con.cursor()
            
            cur.execute("UPDATE STUDENTSMASTER   SET admissionnumber = '{}',AdmissionYear='{}',Name = '{}',ADDRESS = '{}',\
               MOBILE = '{}',COURSE = '{}',DEPARTMENTCODE='{}' WHERE ADMISSIONNUMBER = '{}';".format(str_admissionnumber,str_admissionyear,
               str_name,str_address,str_mobile,str_course,str_department,str_studentadm))   
            con.commit()
            msg = "Record successfully Updated"

      except:
         con.rollback()
         msg = "error in Update operation"
      
      finally:
         return redirect("/students/?msg="+msg)
         return render_template("result.html",msg = msg)
         con.close()



if __name__ == '__main__':
   app.run()