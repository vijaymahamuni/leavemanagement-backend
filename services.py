from operator import attrgetter
from flask import Flask
from tkinter import *
from tkinter import messagebox
from flask_cors import CORS, cross_origin
from flask import Flask, flash, render_template, request, redirect, url_for, session, send_file
from flask_mysqldb import MySQL
from flaskext.mysql import MySQL
from flask import jsonify, send_file
from werkzeug.utils import secure_filename
import pymysql
import re
import os
import calendar
import math
import json
from datetime import timedelta
from flask import Flask
from flask_mail import Mail, Message
import secrets
import string
import uuid
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import datetime
import jwt
app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'vijaysethu0101@gmail.com'
app.config['MAIL_PASSWORD'] = 'yolcoblhomabygxx'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


UPLOAD_FOLDER = '/Project/Front_end/src/images/'
cors = CORS(app, resources={r'*': {'origins': '*'}})
app.config['UPLOAD_FOLDER'] = '/Project/Front_end/src/images/'
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Vijay@#Devr'
app.config['MYSQL_DATABASE_DB'] = 'emp_register'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app)
mysql.init_app(app)


mail = Mail(app) 
app.config['SECRET_KEY'] = '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'


@app.route('/sso_login', methods=['POST'])
def sso_login():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    data = request.get_json()
    email =  data['token']['email']
    str1 = f"""SELECT * FROM employee_data where email='{email}' and  Active_Status='true' ;"""
    cur.execute(str1)
    Ssologin = cur.fetchall()
    conn.commit()
    if len(Ssologin) != 0:
        return jsonify({'message': 'Login successful','data':Ssologin ,'status':200})
    else:
        return jsonify({'message': 'Unauthorized email','status':401})
@app.route('/data', methods=['POST', 'GET'])
def register():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json
      
        email = data['values']['email']
        selected_level = data['selectedLevel']
        employee_id = data['employeeId']
        country =data['country']
        str1 = f"""SELECT * FROM employee_data where email='{data['values']['email']}';"""
        cur.execute(str1)
        account = cur.fetchone()
        if account:
            return jsonify({'status': 400, 'msg': 'enter valid email'})
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return jsonify({'status': 200, 'msg': 'Invalid email address !'})
        else:
            cur.execute(
                f"""INSERT INTO employee_data(firstname,lastname,email,mobileno,country,city,password,gender,profile,AccessLevel,employeeId) VALUES('{data['values']['firstname']}','{data['values']['lastname']}','{data['values']['email']}','{data['values']['mobileno']}','{data['country']}','{data['values']['city']}','{data['values']['password']}','{data['values']['gender']}','/Project/Front_end/src/images/{data['values']['profile']}','{data['selectedLevel']}','{data['employeeId']}'); """)
            conn.commit()
            return jsonify({'status': 200, 'msg': 'Successfully Register!'})
@app.route('/pagelogin', methods=['POST'])
def page():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    data = request.json
    
    str = f"""SELECT * FROM employee_data where email='{data['values']['email']}' and password='{data['values']['password']}' and Active_Status='true' ;"""
    cur.execute(str)
    Talk=str.split()
  
    index=Talk[9]

    data = cur.fetchall()

    if len(data) != 0:
        return jsonify({'status': '200', 'msg': 'Successful login','data':data})
    else: 
        return jsonify({'status': '700', 'msg': 'Incorrect email / password Or Your Account has been Deactivated'})
    




@app.route('/profile_data',methods=['GET'])  
def profile_data():
     conn = mysql.connect()
     cur = conn.cursor(pymysql.cursors.DictCursor)
     str=f"""SELECT * FROM employee_data where Approved=0;"""
     cur.execute(str)
     loginData = cur.fetchall()
     conn.commit()
     
     return jsonify({'data':loginData})
   
            
   
         
@app.route('/userslist/<id>/<int:page>', methods=['GET', 'PUT'])
@app.route('/images/page/<int:page>')
def user(id, page):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
      
    if request.method == 'PUT':
        data = request.json

        str1 = f"""SELECT * FROM employee_data where id !='{data["id"]}' and email='{data["email"]}';"""
        cur.execute(str1)
        edit = cur.fetchone()
        if edit:
            return jsonify({'status': 100, 'msg': 'already mail id exist!'})
        else:
            str = f"""update employee_data set firstname='{data["firstname"]}',lastname='{data["lastname"]}',email='{data["email"]}',mobileno='{data["mobileno"]}',country='{data["country"]}',city='{data["city"]}',password='{data["password"]}',gender='{data["gender"]}',profile='{data["newprofile"]}' ,AccessLevel='{data['selectedLevel']}' ,employeeId='{data['employeeId']}' WHERE id='{data["id"]}';"""
            
            cur.execute(str)
            conn.commit()
            return jsonify({'status': 200, 'msg': 'Updated Successfull!'})
        
    else:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        str1 = "SELECT COUNT(*) FROM employee_data where Approved='0'"
        cur.execute(str1)
        item = cur.fetchall()
        
        PER_PAGE = 5
        if page == 0:
            page = 1
        else:
            page = page
        offset = ((int(page)-1) * PER_PAGE)
        
        str = (f"""SELECT * FROM employee_data where Approved=0 LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
        cur.execute(str)
        data = cur.fetchall()
        conn.commit()
        
        str7 = (f"""SELECT * FROM employee_data where Approved=0""" )
        cur.execute(str7)
        listing = cur.fetchall()
        conn.commit()
      
        return jsonify({'data': data, 'count': item[0]['COUNT(*)'],'excel':listing})
@app.route('/usersdel/<id>', methods=['DELETE'])
def Employee(id):
   
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    str = f"""update employee_data set Approved=1 WHERE id='{id}';"""
  
    cur.execute(str)
    conn.commit()
    return jsonify({'status': 200, 'msg': 'Deleted Successfully!'})
@app.route('/userStatus/<id>', methods=['PUT'])
def vjstatus(id):
    data = request.json
  
    v1=data["SendStatus"]
   
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    str = f"""update employee_data set  Active_Status='{data["SendStatus"]}' WHERE id='{id}';"""
   
    cur.execute(str)
    conn.commit()
    return jsonify({'status': 200, 'msg': 'status update!'})
    

@app.route('/images/<id>', methods=['POST', 'GET'])
def image(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        files = request.files
        file = files.get('file')
    
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        path_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
       
        str = f"""update employee_data set profile='{path_file}' WHERE id='{id}';"""
        
        cur.execute(str)
        conn.commit()
        return jsonify({"img_data": 'success'})
    else:
        str1 = f"""select profile From employee_data WHERE id='{id}';"""
       
        cur.execute(str1)
        img = cur.fetchone()
      
        return send_file(img['profile'], mimetype='multipart/form-data')
@app.route('/photo', methods=['POST', 'GET'])
def photo():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        files = request.files
        file = files.get('file')
     
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        path_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
 
    return jsonify({"img_data": 'path_file'})

@app.route('/employee_list/<id>/<int:page>', methods=['GET', 'PUT'])
@app.route('/images/page/<int:page>')
def employee(id, page):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'PUT':
        data = request.json
 
        str1 = f"""SELECT * FROM employee_data where id !='{data["id"]}' and email='{data["email"]}';"""
        cur.execute(str1)
        edit = cur.fetchone()
        if edit:
            return jsonify({'status': 100, 'msg': 'already mail id exist!'})
        else:
            str = f"""update employee_data set firstname='{data["firstname"]}',lastname='{data["lastname"]}',email='{data["email"]}',mobileno='{data["mobileno"]}',country='{data["country"]}',city='{data["city"]}',password='{data["password"]}',gender='{data["gender"]}',profile='{data["profile"]}' WHERE id='{data["id"]}';"""
           
            cur.execute(str)
            conn.commit()
            return jsonify({'status': 200, 'msg': 'Updated Successfull!'})
    else:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        str1 = "SELECT COUNT(*) FROM employee_data"
        cur.execute(str1)
        item = cur.fetchall()
        
        PER_PAGE = 6
        offset = ((int(page)-1) * PER_PAGE)
       
        str = (f"""SELECT * FROM employee_data where Approved=0 LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
        cur.execute(str)
        data = cur.fetchall()
        conn.commit()
       
        return jsonify({'data': data, 'count': item[0]['COUNT(*)']})
    
@app.route('/get_exceldata',methods=['GET'])
def exportexcel():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    str = (f"""SELECT * FROM employee_data where Approved=0 """ )
    cur.execute(str)
    data = cur.fetchall()
    conn.commit()
    
    return jsonify({'data': data})
         
    
@app.route('/chart_user',methods=['POST'])
def chart_user():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json
        print("get data:",data)
        str2="SELECT DATE_FORMAT(date, '%m') AS date, COUNT(CASE WHEN status = '1' THEN 1 END) AS Present, COUNT(CASE WHEN status = '2' THEN 1 END) AS Absent, COUNT(CASE WHEN status = '3' THEN 1 END) AS Off FROM emp_register.daily_mainentry WHERE DATE_FORMAT(date, '%Y') = '2024' GROUP BY DATE_FORMAT(date, '%m')ORDER BY date LIMIT 0, 1000"

        cur.execute(str2)
        item2 = cur.fetchall()
        conn.commit()
        print("item2",item2)
        days_in_months = (1,12)
        a=[]
        size=len(item2)
        
    for month, num_days in enumerate(days_in_months, start=1):
        x=[*range(num_days)]
        if(month==2):
            for day in x :
                if size != 0 :
                    
                    day2=day+1
                 
                    if(day2<10):
                        day2='0'+str(day2)
                        
                    else:
                        day2=day2    
                    arr=[item for item in item2 if item.get('date')== str(day2)]
                    
                    if len(arr) == 0:
                            attendance = {'date':str(day2),'Present':0,'Absent':0,'Off':0}
                            item2.append(attendance)
                else :
                    day1=int(day)+1
                    if day1 < 10:
                        day1='0'+str(day1)
                        
                    else:
                        day1=day1
                           
                    if int(day1):
                        attendance = {'date':str(day1),'Present':0,'Absent':0,'Off':0}
                        a.append(attendance)
               
    if len(item2) == 0 :                
        item2=a
    # item2.sort(key=attrgetter('date'))
    
    item2 = sorted(item2, key=lambda x: x['date'])
    for item in item2:
       month_number = int(item['date'])
       month_name = calendar.month_abbr[month_number]
       item['date'] = month_name


    
    return jsonify({'data': item2})
@app.route('/date_picker',methods=['POST'])
def datewise_picker():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json
        
        str2="SELECT COUNT(DISTINCT(userid))as count FROM  emp_register.daily_mainentry"
        cur.execute(str2)
        item1 = cur.fetchall()
        conn.commit()
       
        user_limit = item1[0]['count']
     
        date_picker=data['date_picker']
        Month=data['Month']
        Pass=data['year_pass']
        str_month= str(Month[0])
        str_year= str(Pass[0])
        int_month=int(str_month)
        select_month=int_month+1
        print("get year or not",type(str_year))


        select_strmonth='0'+str(select_month)
        if(date_picker==''):
            str3="SELECT b.firstname,b.lastname,MONTH(a.date) AS Month,YEAR(a.date) AS Year,COUNT(CASE WHEN a.status = '1' THEN 1 END) AS Present,COUNT(CASE WHEN a.status = '2' THEN 1 END) AS Absent,COUNT(CASE WHEN a.status = '3' THEN 1 END) AS Off FROM emp_register.daily_mainentry AS a LEFT JOIN emp_register.employee_data AS b ON a.userid = b.id WHERE     YEAR(a.date) = '"+str_year+"' AND MONTH(a.date) = '"+select_strmonth+"' GROUP BY b.firstname,b.lastname,YEAR(a.date),MONTH(a.date)ORDER BY b.firstname,YEAR(a.date),MONTH(a.date)"
           

        else:
            date_object = datetime.strptime(date_picker, '%Y-%m-%dT%H:%M:%S.%fZ')
            just_date = date_object.date()
            just_date_string = str(just_date)
            
            str3="SELECT a.id,a.userid,a.date,a.status,b.firstname,b.lastname ,Month(date) as Month,( select count(*)  from emp_register.daily_mainentry p where status='1' and p.date=a.date and p.userid=a.userid ) as Present,( select count(*)  from emp_register.daily_mainentry v where status='2' and v.date=a.date  and v.userid=a.userid) as Absent,(select count(*)  from emp_register.daily_mainentry o where status='3' and o.date=a.date and o.userid=a.userid) as Off from emp_register.daily_mainentry as a left join emp_register.employee_data as b on a.userid = b.id   where date='"+ just_date_string +"'  "
        
        cur.execute(str3)
        item2 = cur.fetchall()
        conn.commit()
        days_in_months = (1,user_limit)
        a=[]
        size=len(item2)
    if(date_picker==''):
          item2=item2
    else:
        for month, num_days in enumerate(days_in_months, start=1):
         x=[*range(num_days)]
         if(month==2):
            for day in x :
                
                  if size != 0 :
                    day=day+1  
                    arr=[item for item in item2 if item.get('userid')== (day)]
                    
                    if len(arr) == 0:
                       attendance = {'userid':str(day),'Present':0,'Absent':0,'Off':0,'firstname':str(day)}
                       item2.append(attendance)
                  else :
                    day1=int(day)+1
                    
                           
                    if int(day1):
                        attendance = {'userid':str(day1),'Present':0,'Absent':0,'Off':0,'firstname':str(day1)}
                        a.append(attendance)
               
                            
                            
                     
                    
    if len(item2) == 0 :                
        item2=a
   
    # item2.sort(key=attrgetter('userid'))
 
    # item2 = sorted(item2, key=lambda x: x['userid'])

    return jsonify({'data': item2})

@app.route('/year_userwise',methods=['POST'])
def yearly_userwise():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json
        filter_year=data['year_pass']
        str_filter_year= str(filter_year[0])
        str2="SELECT COUNT(DISTINCT(userid))as count FROM  emp_register.daily_mainentry"
        cur.execute(str2)
        item1 = cur.fetchall()
        conn.commit()
      
        user_limit = item1[0]['count']
       
        str4="SELECT a.id,a.userid,a.date,a.status,b.firstname,b.lastname,MONTH(a.date) AS Month,YEAR(a.date) AS Year,(SELECT COUNT(*) FROM emp_register.daily_mainentry p WHERE p.status = '1' AND p.userid = a.userid) AS Present,(SELECT COUNT(*) FROM emp_register.daily_mainentry v WHERE v.status = '2' AND v.userid = a.userid) AS Absent,(SELECT COUNT(*) FROM emp_register.daily_mainentry o WHERE o.status = '3' AND o.userid = a.userid) AS Off FROM emp_register.daily_mainentry AS a LEFT JOIN  emp_register.employee_data AS b ON a.userid = b.id WHERE YEAR(a.date) = '"+str_filter_year+"' GROUP BY a.id, a.userid, a.date, a.status, b.firstname, b.lastname, Month, Year"    
        cur.execute(str4)
        item2 = cur.fetchall()
        conn.commit()
        days_in_months = (1,user_limit)
        a=[]
        size=len(item2)
       
    for month, num_days in enumerate(days_in_months, start=1):
        x=[*range(num_days)]
        if(month==2):
            for day in x :
                
                  if size != 0 :
                    day=day+1  
                    arr=[item for item in item2 if item.get('userid')== (day)]
                    
                    if len(arr) == 0:
                       attendance = {'userid':str(day),'Present':0,'Absent':0,'Off':0,'firstname':str(day)}
                       item2.append(attendance)
                  else :
                    day1=int(day)+1
                    
                           
                    if int(day1):
                        attendance = {'userid':str(day1),'Present':0,'Absent':0,'Off':0,'firstname':str(day1)}
                        a.append(attendance)
               
                            
                            
                     
                    
    if len(item2) == 0 :                
        item2=a
   
    # item2.sort(key=attrgetter('userid'))

    # item2 = sorted(item2, key=lambda x: x['userid'])
    
    return jsonify({'data': item2})
@app.route('/UsersDropdown', methods=['GET'])
def UsersDropdown():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    str1 = "SELECT firstname FROM emp_register.employee_data where Active_Status='True'"
    cur.execute(str1)
    OverallUsers = cur.fetchall()
   
    return jsonify({'data': OverallUsers})
   
@app.route('/summary', methods=['POST'])
def month():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json
        User = data['User']
        Month=data['Month']
        Pass=data['year_pass']
        print("pass year printed",Pass)
        str_user= str(User[0])
        str_month= str(Month[0])
        str_year= str(Pass[0])
        int_month=int(str_month)
        int_user=int(str_user)
        select_month=int_month+1
        select_strmonth='0'+str(select_month)
        select_user=int_user
        employee=str(select_user)
       
        year_of_select=str(str_year)
        if(employee=='0'):
            str1 = "SELECT  DATE_FORMAT(date,'%d') AS date,(select count(*) from  daily_mainentry p where status='1' and p.date=c.date )as Present,(select count(*)  from daily_mainentry a where status='2' and a.date=c.date ) as Absent,(select count(*)  from daily_mainentry o where status='3' and o.date=c.date  ) as Off  from daily_mainentry c  where date_format(date,'%m')='"+select_strmonth+"' and date_format(date,'%Y')='"+year_of_select+"'  group by date"
        else:
            str1= "SELECT  DATE_FORMAT(date,'%d') AS date,userid,(select count(*) from  daily_mainentry p where status='1' and p.date=c.date and p.userid=c.userid )as Present,(select count(*)  from daily_mainentry a where status='2' and a.date=c.date and a.userid=c.userid) as Absent,(select count(*)  from daily_mainentry o where status='3' and o.date=c.date and o.userid=c.userid) as Off  from daily_mainentry c  where date_format(date,'%m')='"+select_strmonth+"' and date_format(date,'%Y')='"+str_year+"' and userid='"+employee+"'  group by date"
    
    cur.execute(str1)
    item2 = cur.fetchall()
    conn.commit()
    after_add= select_month
    year1=2024
    days_in_months = calendar.monthrange(year1,after_add)[1]
    a=[]
    size=len(item2)

    if not item2:
        item2 = [{'date': str(day).zfill(2), 'Present': 0, 'Absent': 0, 'Off': 0} for day in range(1, days_in_months + 1)]
    else:
        existing_dates = set(item['date'] for item in item2)
        for day in range(1, days_in_months + 1):
            str_day = str(day).zfill(2)  
            if str_day not in existing_dates:
                item2.append({'date': str_day, 'Present': 0, 'Absent': 0, 'Off': 0})
    item2 = sorted(item2, key=lambda x: x['date'])
  
    return jsonify({'data': item2})

  
@app.route('/bar_click', methods=['POST'])
def barchart():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json
  
        User = data['popup_date']
        Month=data['Month']
        Pass=data['year_pass']


        str_user= str(User)
        str_month= str(Month[0])
        str_year= str(Pass[0])
        int_month=int(str_month)
        int_user=int(str_user)
        select_month=int_month+1
        select_strmonth='0'+str(select_month)
        select_user=int_user
        employee=str(select_user)
        
        year_of_select=str(str_year)
        str1="SELECT a.id,a.userid,a.status,b.firstname,b.lastname ,Month(date) as Month from daily_mainentry   as a left join employee_data as b on a.userid = b.id where date_format(date,'%m')='"+select_strmonth+"' and date_format(date,'%d')='"+str_user+"' and date_format(date,'%Y')='"+str_year+"'"
        cur.execute(str1)

        item2 = cur.fetchall()
        conn.commit()

        newdict={}
        pre=[]
        absents=[]
        offf=[]
        
        for i in item2:
           
            if i['status']==1:
                pre.append(i['firstname'])
            elif i['status']==2:
                absents.append(i['firstname'])
            
        newdict={
                'Present':pre,
                'Absent':absents,
                'Off':offf
    
        }     
     
        item2=newdict
       
    
        return jsonify({'data': item2})



@app.route('/email', methods=['POST'])
def index():
    if request.method == 'POST':
        data = request.json
       
        Name= data['name']
        Email=data['email']
        Subject=data['subject']
        Msg=data['Message']

        recipient='vijaysethu0101@gmail.com'
       
    msg1 = Message(Subject, sender='vijaysethu0101@gmail.com', recipients=[recipient])   
    msg2 = Message(Subject, sender='vijaysethu0101@gmail.com', recipients=[Email])
    msg1.html=render_template('emailTemplate.html', name=Name,email=Email,message=Msg,subject=Subject)
    msg2.html = render_template('adminTemplate.html')
    messages=[msg1,msg2]
    for msg in messages:
        mail.send(msg)
    return "Sent"




@app.route('/ticketList', methods=['POST','GET'])
def email_list():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json
     
        Name= data['name']
        Email=data['email']
        Subject=data['subject']
        Msg=data['Message']
        mainName=data['mainName']

        res = [ sub['From_email'] for sub in Email ]
        id = uuid.uuid1()
        userid=id.hex
        res_addname = [ sub['newName'] for sub in Email ]
       
        str1=(f"""INSERT INTO contact_data(id,subject,message,name) VALUES('{userid}','{Subject}','{Msg}','{mainName}'); """)
        cur.execute(str1)
        new_email=res
        for mes,addname in zip(new_email,res_addname):
            str3 =(f"""INSERT INTO main_table(ticketid,email,name)VALUES('{userid}','{mes}','{addname}')""")
            cur.execute(str3)
            conn.commit() 
        for message in new_email:
            user_email=message
            msg = Message(Subject, sender='vijaysethu0101@gmail.com', recipients=[user_email])
            msg.html = render_template('mainTemplate.html')
            mail.send(msg)
            return jsonify({'status': 200, 'msg': 'inserted Successfully!'})  
    else:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        str = (f"""SELECT id,subject,message,name from  contact_data where flag=0 """)
        cur.execute(str)
        data = cur.fetchall()
        conn.commit()
        
        return jsonify({'data': data})
    
   
    return "sent"
@app.route('/ticketEdit/<id>', methods=['GET'])
def edit_ticket(id):
 
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    str1 = (f"""SELECT id,ticketid,email,name from  main_table  where ticketid='{id}'""")
    cur.execute(str1)
    data = cur.fetchall()
  
    conn.commit()
    str = (f"""SELECT id,subject,message,name from  contact_data  where id='{id}'""")
    cur.execute(str)
    ticket = cur.fetchall()
    conn.commit()
    return jsonify({'data': data,'ticket':ticket})

    return "sent"
@app.route('/deleteTicketlist/<id>',  methods=['PUT'])
def deleted_ticketlist(id):
 
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    str = f"""update contact_data set flag=1 WHERE id='{id}';"""
   
    cur.execute(str)
    conn.commit()
    return jsonify({'status': 200, 'msg': 'Deleted Successfully!'})
       
         
@app.route('/updateTicket/<id>',  methods=['PUT'])
def update_ticket(id):
   
    data = request.json
 
    Email=data[0]['Email_List']
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    update_name = data[0]['Name']
    update_subject = data[0]['Subject']
    update_msg = data[0]['Msg']
    update_mainid=data[0]['emaildata_id']
    update_mainName=data[0]['updateName']
  
    res_email = [ sub['From_email'] for sub in Email ]

    res_email1 = [ sub['newName'] for sub in Email ]

    selectRemoveid=data[0]['SelectRemoveid']

    deleteId = ''.join(selectRemoveid)
  
    
    new_list = res_email1[1:]
   
    str8 = (f"""SELECT email from  main_table  where ticketid='{id}'""")
    cur.execute(str8)
    data1 = cur.fetchall()
    conn.commit()
      
    upto_name=len(data1)
   
    new_emaillist= res_email[upto_name:]
    
    list_values = update_mainid.split(",")
    
    str = f"""update contact_data set subject='{update_subject}',message='{update_msg}',name='{update_mainName}'  WHERE id='{id}';"""
   
    cur.execute(str)
    conn.commit()
    for updatename, main_id in zip(res_email1, list_values):
    
        str1 = f"""update main_table set name='{updatename}'  WHERE  ticketid='{id}' and id='{main_id}';"""
        
        cur.execute(str1)
        conn.commit()
    str7=f"""DELETE FROM main_table  WHERE ticketid='{id}' and id='{deleteId}' ;"""
    cur.execute(str7)
    data = cur.fetchall()
    conn.commit()
   
    # upto_name=len(data)
 
    # selectEmailid= [ sub['id'] for sub in data ]
  
    # not_equal_values = (set(res_email).difference(selectEmailid))

    # sentMEailtemp=list(not_equal_values)

   
    for i in range(len(res_email) - len(list_values)):
     list_values.append('')

    for tic_emailid, main_id ,newname in zip(res_email, list_values,res_email1):
        str4=(f""" INSERT INTO main_table (email,ticketid,name) SELECT '{tic_emailid}','{id}','{newname}' WHERE NOT EXISTS (SELECT * FROM emp_register.main_table WHERE id = '{main_id}');""")
        cur.execute(str4)
        conn.commit()        
    
    return jsonify({'status': 200, 'msg': 'Updated Successfully!'})  

@app.route('/deleteEmailticket/<id>',  methods=['PUT'])
def delete_emailtic(id):
    data = request.json

    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    flag_value = data[0]['flag']
    removeid=data[0]['SelectedRemoveid']

    my_Removeid = ', '.join(removeid)

    my_list = flag_value.split(",")

    str3=f"""DELETE FROM main_table  WHERE ticketid='{id}' and id='{removeid}' ;"""
    cur.execute(str3)
    conn.commit()  
    return jsonify({'status': 200, 'msg': 'Deleted Successfully!'})         

@app.route('/viewPage/<id>', methods=['GET'])
def viewUser_details(id):

    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    str1 = (f"""select * From  employee_data  where id='{id}'""")
    cur.execute(str1)
    data = cur.fetchall()
  
    conn.commit()
    return jsonify({'data': data})


@app.route('/changePassword', methods=['POST','PUT'])
def changePassword():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json
    
        new_password = data['newpassword']
        profile_id = data['Profileid']
        profile_email=data['ProfileEmail']

        str1 = f"""update employee_data set password='{new_password}'  WHERE  id='{profile_id}';"""
        cur.execute(str1)
        cur.fetchall()
        conn.commit()
        subject='Change Password'
        msg = Message(subject,sender='vijaysethu0101@gmail.com', recipients=[profile_email])
        msg.html = render_template('changepassword.html')
        mail.send(msg)

        return jsonify({'status': 200, 'msg': 'change password Successfully!'})   
    else:
        data = request.json

        newPassword=data['forgotnewpass']
        resetOtp=data['resetOtp']

        str1 = f"""update employee_data set password='{newPassword}'  WHERE  forgotpassword='{resetOtp}';"""
        cur.execute(str1)
        cur.fetchall()
        conn.commit()
        return jsonify({'status':200, 'msg': 'Updated Successfully!'})  
        
@app.route('/forgotPassword' ,methods=['POST'])
def generate_code():
    length=6
    characters = string.ascii_letters + string.digits
    code = ''.join(secrets.choice(characters) for _ in range(length))
  
    data = request.json

    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    email_value = data['email']

    str=(f"""select * From  employee_data  where email='{email_value}'""")
    cur.execute(str)
    Checkemail = cur.fetchall()

    if(Checkemail !=()):
           str1 = f"""update employee_data set forgotpassword ='{code}' WHERE email='{email_value}';"""
           cur.execute(str1)
           cur.fetchall()
           conn.commit()

           subject='Reset Password'
           msg = Message(subject,sender='vijaysethu0101@gmail.com', recipients=[email_value])
           msg.html = render_template('forgot password.html',OTP=code)
           mail.send(msg)
   
     
    
           return jsonify({'status': 200, 'msg': 'reset Password!','Otp_code':code})
 
    else:
        return jsonify({'status': 500, 'msg': 'Emailid incorrect'})
    
    
@app.route('/kpi_data',methods=['POST'])
def kpi_data():
    data = request.json

    conn = mysql.connect()
    monthly = data['Month']
    yearly =data['year_kpi'][0]
    
    my_int = int(monthly[0])
    newmonth = my_int +1

    kpi_putmonth=str(newmonth)
    str_monthly='0'+str(kpi_putmonth)

    str_yearly=str(yearly)

    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
       str1="SELECT MAX(a.id) AS id,MAX(a.userid) AS userid,MAX(a.status) AS status,MAX(b.firstname) AS firstname,MAX(b.lastname) AS lastname,MONTH(MAX(a.date)) as Month,SUM(CASE WHEN a.status='1' THEN 1 ELSE 0 END) AS Present,SUM(CASE WHEN a.status='2' THEN 1 ELSE 0 END) AS Absent,SUM(CASE WHEN a.status='3' THEN 1 ELSE 0 END) AS Off FROM emp_register.daily_mainentry AS a LEFT JOIN emp_register.employee_data AS b ON a.userid = b.id WHERE DATE_FORMAT(a.date, '%m') ='"+str_monthly+"' AND DATE_FORMAT(a.date, '%Y') ='"+str_yearly+"' GROUP BY a.userid ORDER BY Present DESC LIMIT 3;"    
       cur.execute(str1)
       item2 = cur.fetchall()
       conn.commit()

       str2="SELECT MAX(a.id) AS id,MAX(a.userid) AS userid,MAX(a.status) AS status,MAX(b.firstname) AS firstname,MAX(b.lastname) AS lastname,MONTH(MAX(a.date)) as Month,SUM(CASE WHEN a.status='1' THEN 1 ELSE 0 END) AS Present,SUM(CASE WHEN a.status='2' THEN 1 ELSE 0 END) AS Absent,SUM(CASE WHEN a.status='3' THEN 1 ELSE 0 END) AS Off FROM emp_register.daily_mainentry AS a LEFT JOIN emp_register.employee_data AS b ON a.userid = b.id WHERE DATE_FORMAT(a.date, '%m') ='"+str_monthly+"' AND DATE_FORMAT(a.date, '%Y') ='"+str_yearly+"' GROUP BY a.userid  ORDER BY Absent desc LIMIT 3;"    
       cur.execute(str2)
       item3 = cur.fetchall()
       conn.commit()

       str3="SELECT  DATE_FORMAT(date, '%b %e, %Y') AS date, DAYNAME(date) AS day_name,(select count(*) from  emp_register.daily_mainentry p where status='1' and p.date=c.date )as Present,(select count(*)  from emp_register.daily_mainentry a where status='2' and a.date=c.date ) as Absent,(select count(*)  from emp_register.daily_mainentry o where status='3' and o.date=c.date  ) as Off  from emp_register.daily_mainentry c where date_format(date,'%m')='"+str_monthly+"'and date_format(date,'%Y')='"+str_yearly+"' group by date ORDER BY Present desc limit 1;"    
       cur.execute(str3)
       item4 = cur.fetchall()
       conn.commit()

       str4="SELECT  DATE_FORMAT(date, '%b %e, %Y') AS date, DAYNAME(date) AS day_name,(select count(*) from  emp_register.daily_mainentry p where status='1' and p.date=c.date )as Present,(select count(*)  from emp_register.daily_mainentry a where status='2' and a.date=c.date ) as Absent,(select count(*)  from emp_register.daily_mainentry o where status='3' and o.date=c.date  ) as Off  from emp_register.daily_mainentry c where date_format(date,'%m')='"+str_monthly+"'and date_format(date,'%Y')='"+str_yearly+"' group by date ORDER BY Absent desc limit 1;"    
       cur.execute(str4)
       item5 = cur.fetchall()
       conn.commit()

       return jsonify({'data': item2,'Absent':item3,'Most_preDay':item4,'Most_absentDay':item5}) 
@app.route('/yearlyWise_kpi',methods=['POST'])
def yearlyWise_Kpi():
    data = request.json

    yearly =data['year_kpi'][0]
    str_yearly=str(yearly)

    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
       str1="SELECT a.id,a.userid,a.date,a.status,b.firstname,b.lastname ,Month(date) as Month,(select count(*)from emp_register.daily_mainentry p where status='1' and  p.userid=a.userid )as Present  from emp_register.daily_mainentry as a left join emp_register.employee_data as b on a.userid = b.id where date_format(date,'%Y')='"+str_yearly+"' group by userid ORDER BY Present desc LIMIT 3;"    
       cur.execute(str1)
       item2 = cur.fetchall()
       conn.commit()
 
       str2="SELECT a.id,a.userid,a.date,a.status,b.firstname,b.lastname ,Month(date) as Month,( select count(*)  from emp_register.daily_mainentry v where status='2'and v.userid=a.userid ) as Absent from emp_register.daily_mainentry as a left join emp_register.employee_data as b on a.userid = b.id where date_format(date,'%Y')='"+str_yearly+"' group by userid ORDER BY Absent desc LIMIT 3;"    
       cur.execute(str2)
       item3 = cur.fetchall()
       conn.commit()

       str3="SELECT  DATE_FORMAT(date, '%b %e, %Y') AS date, DAYNAME(date) AS day_name,(select count(*) from  emp_register.daily_mainentry p where status='1' and p.date=c.date )as Present from emp_register.daily_mainentry c where date_format(date,'%Y')='"+str_yearly+"'group by date ORDER BY Present desc limit 1;"    
       cur.execute(str3)
       item4 = cur.fetchall()
       conn.commit()

       str4="SELECT  DATE_FORMAT(date, '%b %e, %Y') AS date, DAYNAME(date) AS day_name,(select count(*)  from emp_register.daily_mainentry a where status='2' and a.date=c.date ) as Absent from emp_register.daily_mainentry c where date_format(date,'%Y')='"+str_yearly+"' group by date ORDER BY Absent desc limit 1;"    
       cur.execute(str4)
       item5 = cur.fetchall()
       conn.commit()

       return jsonify({'data': item2,'Absent':item3,'Most_preDay':item4,'Most_absentDay':item5})       
      
@app.route('/kpi_datepicker',methods=['POST'])
def kpi_datepicker():
    data = request.json

    conn = mysql.connect()
    week_Start=data['week_start']
    week_End=data['weekend']

    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
       str1="SELECT a.id,a.userid,a.date,a.status,b.firstname,b.lastname ,Month(date) as Month,(select count(*)from emp_register.daily_mainentry p where status='1' and  month(date)=month and p.userid=a.userid and date BETWEEN '"+week_Start+"' AND '"+week_End+"')as Present from emp_register.daily_mainentry   as a left join emp_register.employee_data as b on a.userid = b.id where date='"+week_Start+"' group by userid ORDER BY Present desc LIMIT 3;"    
       cur.execute(str1)
       item2 = cur.fetchall()
       conn.commit()

       str2="SELECT a.id,a.userid,a.date,a.status,b.firstname,b.lastname ,Month(date) as Month,( select count(*)  from emp_register.daily_mainentry v where status='2' and month(date)=month and v.userid=a.userid and date BETWEEN '"+week_Start+"' AND '"+week_End+"') as Absent from emp_register.daily_mainentry   as a left join emp_register.employee_data as b on a.userid = b.id where date='"+week_Start+"' group by userid ORDER BY Absent desc limit 3;"    
       cur.execute(str2)
       item3= cur.fetchall()
       conn.commit()

       str3="SELECT   DATE_FORMAT(date, '%b %e, %Y') AS date, DAYNAME(date) AS day_name,(select count(*) from  emp_register.daily_mainentry p where status='1' and p.date=c.date )as Present from emp_register.daily_mainentry c where date BETWEEN '"+week_Start+"' AND '"+week_End+"' group by date ORDER BY Present desc limit 1"    
       cur.execute(str3)
       item4= cur.fetchall()
       conn.commit()

       str4="SELECT DATE_FORMAT(date, '%b %e, %Y') AS date, DAYNAME(date) AS day_name,(select count(*) from  emp_register.daily_mainentry p where status='2' and p.date=c.date )as Absent from emp_register.daily_mainentry c where date BETWEEN '"+week_Start+"' AND '"+week_End+"' group by date ORDER BY Absent desc limit 1;"    
       cur.execute(str4)
       item5= cur.fetchall()
       conn.commit()

      
    return jsonify({'data': item2,'most_absent':item3,'Most_preDay':item4,'Most_absentDay':item5}) 


@app.route('/report_summary',methods=['POST'])
def report_summary():
    data = request.json

    SelectUser=data['userid'][0]
    select_year=data['selectYear'][0]

    str_User=str(SelectUser)
    str_year=str(select_year)
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        str1="SELECT a.id,a.userid,a.date,a.status,b.firstname,b.lastname ,Month(date) as Month,DATE_FORMAT(date, '%M') AS head_month,(select count(*)  from emp_register.daily_mainentry p where status='1' and  month(date)=month and p.userid=a.userid  ) as Present,( select count(*)  from emp_register.daily_mainentry v where status='2' and  month(date)=month and v.userid=a.userid) as Absent,(select count(*)  from emp_register.daily_mainentry o where status='3' and month(date)=month  and o.userid=a.userid) as Off from emp_register.daily_mainentry   as a left join emp_register.employee_data as b on a.userid = b.id where userid='"+str_User+"' and  date_format(date,'%Y')='"+str_year+"' group by Month order by Month asc"    
        cur.execute(str1)
        item2 = cur.fetchall()
        conn.commit()

        months = [calendar.month_name[i] for i in range(1, 13)]

        a=[]
        size=len(item2)

        # for month, num_days in enumerate(months, start=1):
        for day in months :
                if size != 0 :
                    arr=[item for item in item2 if item.get('head_month')== str(day)]
                    
                    if len(arr) == 0:
                            attendance = {'head_month':str(day),'Present':0,'Absent':0,'Off':0}
                            item2.append(attendance)
                else :
                    if (day):
                        attendance = {'head_month':str(day),'Present':0,'Absent':0,'Off':0}
                        a.append(attendance)
               
    if len(item2) == 0 :                
        item2=a

    # item2.sort(key=attrgetter('date'))

    # item2 = sorted(item2, key=lambda x: x['head_month'])
    
    return jsonify({'data': item2})

@app.route('/monthClick_data', methods=['POST'])
def monthClickdata():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json

        User = data['userid'][0]
        Month=data['selectMonth']
        YearPass=data['selectYear'][0]

        intYear=int(YearPass)
  
        employee= str(User)
        str_month= str(Month)
        str_year=str(YearPass)
        str1= "SELECT  DATE_FORMAT(date,'%d') AS date,DATE_FORMAT(date,'%d') AS head_month,userid,(select count(*) from  daily_mainentry p where status='1' and p.date=c.date and p.userid=c.userid )as Present,(select count(*)  from daily_mainentry a where status='2' and a.date=c.date and a.userid=c.userid) as Absent,(select count(*)  from daily_mainentry o where status='3' and o.date=c.date and o.userid=c.userid) as Off  from daily_mainentry c  where date_format(date,'%M')='"+str_month+"'  and date_format(date,'%Y')='"+str_year+"' and userid='"+employee+"'  group by date"
        cur.execute(str1)
        item2 = cur.fetchall()
        conn.commit()

        month_number = datetime.strptime(str_month, "%B").month
 
        after_add= month_number
        year1=intYear
        days_in_months = calendar.monthrange(year1,after_add)
        a=[]
        size=len(item2)

        for month, num_days in enumerate(days_in_months, start=1):
            x=[*range(num_days)]
  
            if(month==2):
                for day in x :
                
                  if size != 0 :
                    arr=[item for item in item2 if item.get('date')== str(day)]
                    
                    if len(arr) == 0:
                        if day < 10:
                            attendance = {'head_month':'0'+str(day),'Present':0,'Absent':0,'Off':0}
                        else:   
                            attendance = {'head_month':str(day),'Present':0,'Absent':0,'Off':0}
                            item2.append(attendance)
                  else :
                    day1=int(day)+1
                    if day1 < 10:
                        day1='0'+str(day1)
                        
                    else:
                        day1=day1
                           
                    if int(day1):
                        attendance = {'head_month':str(day1),'Present':0,'Absent':0,'Off':0}
                        a.append(attendance)
               
                            
                     
                    
    if len(item2) == 0 :                
        item2=a

    # item2.sort(key=attrgetter('date'))

    item2 = sorted(item2, key=lambda x: x['head_month'])
    
    return jsonify({'data': item2})    

@app.route('/SummaryAll',methods=['POST','PUT'])
def Summary_All():
    data = request.json

    if request.method == 'POST':
        SelectUser=data['userid']
        select_year=data['selectYear'][0]

        str_User=str(SelectUser)
        str_year=str(select_year)
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        str1="SELECT MAX(a.id) AS id, MAX(a.userid) AS userid,MONTH(a.date) AS Month,DATE_FORMAT(a.date, '%M') AS head_month,MAX(a.status) AS status,MAX(b.firstname) AS firstname,MAX(b.lastname) AS lastname,(SELECT COUNT(*) FROM emp_register.daily_mainentry p WHERE status='1' AND MONTH(date)=Month) AS Present,(SELECT COUNT(*) FROM emp_register.daily_mainentry v WHERE status='2' AND MONTH(date)=Month) AS Absent,(SELECT COUNT(*) FROM emp_register.daily_mainentry o WHERE status='3' AND MONTH(date)=Month) AS Off FROM emp_register.daily_mainentry AS a LEFT JOIN emp_register.employee_data AS b ON a.userid = b.id WHERE DATE_FORMAT(a.date,'%Y') = '2023' GROUP BY Month, head_month ORDER BY Month ASC; "    
        cur.execute(str1)
        item2 = cur.fetchall()
        conn.commit()

        months = [calendar.month_name[i] for i in range(1, 13)]

        a=[]
        size=len(item2)

        # for month, num_days in enumerate(months, start=1):
        for day in months :
                if size != 0 :
                    arr=[item for item in item2 if item.get('head_month')== str(day)]
                    
                    if len(arr) == 0:
                            attendance = {'head_month':str(day),'Present':0,'Absent':0,'Off':0}
                            item2.append(attendance)
                else :
                    if (day):
                        attendance = {'head_month':str(day),'Present':0,'Absent':0,'Off':0}
                        a.append(attendance)
               
        if len(item2) == 0 :                
            item2=a

        # item2.sort(key=attrgetter('date'))

        # item2 = sorted(item2, key=lambda x: x['head_month'])
    
        return jsonify({'data': item2})
    else:
        data = request.json

        select_year=data['selectYear'][0]
        Month=data['selectMonth']
        intYear=int(select_year)
        str_year=str(select_year)
        str_month= str(Month)
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        str1= "SELECT  DATE_FORMAT(date,'%d') AS date,DATE_FORMAT(date,'%d') AS head_month,userid,(select count(*) from  daily_mainentry p where status='1' and p.date=c.date ) as Present,(select count(*)  from daily_mainentry a where status='2' and a.date=c.date ) as Absent,(select count(*)  from daily_mainentry o where status='3' and o.date=c.date ) as Off FROM daily_mainentry c WHERE date_format(date,'%M') = '"+str_month+"' and date_format(date,'%Y') = '"+str_year+"' GROUP BY date, head_month, userid ORDER BY date ASC;"
        cur.execute(str1)
        item2 = cur.fetchall()
        conn.commit()
        month_number = datetime.strptime(str_month, "%B").month

        after_add= month_number
        year1=intYear
        days_in_months = calendar.monthrange(year1,after_add)
        a=[]
        size=len(item2)

        for month, num_days in enumerate(days_in_months, start=1):
            x=[*range(num_days)]
   
            if(month==2):
                for day in x :
                
                  if size != 0 :
                    arr=[item for item in item2 if item.get('date')== str(day)]
                    
                    if len(arr) == 0:
                        if day < 10:
                            attendance = {'head_month':'0'+str(day),'Present':0,'Absent':0,'Off':0}
                        else:   
                            attendance = {'head_month':str(day),'Present':0,'Absent':0,'Off':0}
                            item2.append(attendance)
                  else :
                    day1=int(day)+1
                    if day1 < 10:
                        day1='0'+str(day1)
                        
                    else:
                        day1=day1
                           
                    if int(day1):
                        attendance = {'head_month':str(day1),'Present':0,'Absent':0,'Off':0}
                        a.append(attendance)
               
                            
                     
                    
    if len(item2) == 0 :                
        item2=a

    # item2.sort(key=attrgetter('date'))

    item2 = sorted(item2, key=lambda x: x['head_month'])
    
    return jsonify({'data': item2})    

@app.route('/permissionLeave', methods=['POST'])
def permissionLeave():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    data = request.json

    if request.method == 'POST':
        employee=data['Employee']

        Empemail=data['Empid']
        leave_type=data['Leave Type']
        start_date=data['Fromdate']
        end_Date=data['ToDate']
        L1_reqtiming=data['L1Req-timing']
        date_object = datetime.strptime(start_date, '%Y-%m-%d')
        formatted_Startdate = date_object.strftime('%B %d, %Y')
        date_object1 = datetime.strptime(end_Date, '%Y-%m-%d')
        formatted_enddate = date_object1.strftime('%B %d, %Y')
        reqlevel_employee=data['Level_employee']
        levelof_Emp=data['Level_employee']

        if(levelof_Emp=='L4'):
            levelof_Emp='L3'
        elif(levelof_Emp =='L3'):
            levelof_Emp='L2'
        elif(levelof_Emp =='L2'):
            levelof_Emp='L1'

        str=f"""INSERT INTO leave_management(leave_type, start_date, end_date, comments,employeeid,L1_reqtiming) VALUES('{data['Leave Type']}','{data['Fromdate']}','{data['ToDate']}','{data['Commends']}','{data['Profileid']}','{L1_reqtiming}'); """
        cur.execute(str)
        cur.fetchall()
        conn.commit()
        str1=f"""SELECT email,firstname,id FROM emp_register.employee_data
where AccessLevel='{levelof_Emp}'"""
        cur.execute(str1)
        SendLead = cur.fetchall()

        Subject='Leave Request'
        email_values = [d['email'] for d in SendLead]

        teamLeads_names = [d['firstname'] for d in SendLead]
        
        teamLeads_id = [d['id'] for d in SendLead]
        
        result_leadsName=(', '.join(teamLeads_names))
       
        Cur_Employeeid=data['Profileid']
        str2=f"""SELECT id FROM emp_register.leave_management
where employeeid='{Cur_Employeeid}' and Showapprove='0' 
ORDER BY id DESC limit 1"""
        cur.execute(str2)
        viewPageid = cur.fetchall()
        ViewPage_Empid = viewPageid[0]['id']
      
        for message, team_lead_name in zip(email_values, teamLeads_names):
            user_email=message
            msg = Message(Subject,sender=Empemail, recipients=[user_email])
            msg.html = render_template('LeaveReqTemp.html',Employee_name=employee,ViewpageId=ViewPage_Empid,teamLeads_names=team_lead_name,Leave_Type=leave_type,Starting_lev=formatted_Startdate,ending_lev=formatted_enddate,ReqLevel_emp=reqlevel_employee)
            mail.send(msg)
        str6=f"""SELECT id FROM emp_register.leave_management
        ORDER BY id DESC limit 1"""
        cur.execute(str6)
        notificationPageId = cur.fetchall()
        notification_PageId = notificationPageId[0]['id']
        
        request_from=data['Level_employee']  
        ToLevelof_emp=teamLeads_id 
        typeofEmp=data['typeof_notification']
        
        str7="SELECT id FROM emp_register.employee_data where AccessLevel='"+levelof_Emp+"'"
      
        cur.execute(str7)
        SendTeamLead = cur.fetchall()
        SendTeamLead_values = [item['id'] for item in SendTeamLead]
  
        Notification_request= employee +' '+ 'Leave Request'
        for user in SendTeamLead_values:
            str5=f"""INSERT INTO notification_data(message, notification_type, pageId, request_from, request_to) VALUES('{Notification_request}','{typeofEmp}','{notification_PageId}','{request_from}','{user}'); """
            cur.execute(str5)
            cur.fetchall()
            conn.commit()    
       
      
        return jsonify({'status': 200, 'msg': 'Leave Request Sending Succesfully'})
@app.route('/notification/<AllowAccess>/<profileid>', methods=['GET'])
def notification(AllowAccess,profileid):
    Send_notification=AllowAccess
 
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if(Send_notification =='L4'):
         str1 = "SELECT COUNT(*) FROM emp_register.notification_data where request_to='"+profileid+"' and status='0' "
         str2 = "SELECT * FROM emp_register.notification_data where request_to='"+profileid+"'  order by s_no desc "

    elif(Send_notification =='L3'):
        str1 = "SELECT COUNT(*) FROM emp_register.notification_data where request_to='"+profileid+"' and status='0'  "
        str2 = "SELECT * FROM emp_register.notification_data where request_to='"+profileid+"'  order by s_no desc "
   
    elif(Send_notification =='L2'):
        str1 = "SELECT COUNT(*) FROM emp_register.notification_data where request_to='"+profileid+"' and status='0' " 
        str2 = "SELECT * FROM emp_register.notification_data where request_to='"+profileid+"'   order by s_no desc "

    elif(Send_notification =='L1'):
        str1 = "SELECT COUNT(*) FROM emp_register.notification_data where request_to='"+profileid+"'  and status='0'order by s_no desc" 
        str2 = "SELECT * FROM emp_register.notification_data where request_to='"+profileid+"'  order by s_no desc "
     
    
    cur.execute(str1)
    total_pending = cur.fetchall()
 
    cur.execute(str2)
    notificationData = cur.fetchall()
    conn.commit()
   
    return jsonify({'status': 200,'data':notificationData ,'L3notification': total_pending[0]['COUNT(*)']})
@app.route('/notificationUpdate/<id>/<AllowAccess>/<profileid>', methods=['PUT'])
def notificationUpdate(id,AllowAccess,profileid):
    
    Send_notification=AllowAccess
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    data = request.json
    update_status=data['Update_status']
    str = f"""update notification_data set status='{update_status}' where pageId='{id}' and request_to='{profileid}'"""

    cur.execute(str)
    conn.commit()
    str1 = "SELECT COUNT(*) FROM emp_register.notification_data where request_to='"+Send_notification+"' and status='0' and request_to='"+profileid+"'"
  
    cur.execute(str1)
    total_pending = cur.fetchall()

    str2 = "SELECT * FROM emp_register.notification_data where request_to='"+Send_notification+"' and request_to='"+profileid+"' order by s_no desc "
    cur.execute(str2)
    notificationData = cur.fetchall()
    conn.commit()
 
   
  
    return jsonify({'status': 200, 'msg': 'Updated Successfull!','data':notificationData ,'L3notification': total_pending[0]['COUNT(*)']}) 
@app.route('/leaveListing/<tab>', methods=['POST'])
def Leavelisting(tab):
      conn = mysql.connect()
      cur = conn.cursor(pymysql.cursors.DictCursor)
      data = request.json
   
      id=data['employeeId']
      AllowAccess=data['Emp_level']
      Typesofrecords=data['paginationId']
      page=data['current_Page']
      filterUserid=data['selectedUser']
      filterStatus=data['selectedStatus']
      filterDate=data['selectedDate']
      pass_newdate='All'
      apply_filterdate=''
      if(filterDate ==None  or filterDate=='null' or filterDate=='NaN-NaN-NaN'):
        filterDate=pass_newdate
        apply_filterdate = pass_newdate

      else:
        filterDate=filterDate   
        apply_filterdate = filterDate
         

      str1 = "SELECT COUNT(*) FROM emp_register.leave_management where Showapprove=0"
      cur.execute(str1)
      count = cur.fetchall()
      PER_PAGE = 5
      offset = ((int(page)-1) * PER_PAGE)
      if(Typesofrecords == 'Own'):
           str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.employeeid='{id}' ORDER BY id DESC LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
           str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and  a.employeeid='{id}'""")
       
      elif(Typesofrecords =='Requested'):
         if(AllowAccess =='L3' and filterUserid=='All'and filterStatus =='All' and filterDate=='All' ):
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel ='L4' and a.Active_Status='pending' ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel ='L4' and a.Active_Status='pending' """)
         elif(AllowAccess =='L3' and filterUserid !='All' and filterStatus =='All' and filterDate=='All' ):
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.employeeid='{filterUserid}'  and
(a.Showapprove = 0 and AccessLevel ='L4' and a.Active_Status='pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel ='L4' and a.Active_Status='pending' """)
         elif(AllowAccess =='L3' and filterStatus !='All' and  filterUserid=='All' and  filterDate=='All'):
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.Active_status='{filterStatus}' and
(a.Showapprove = 0 and AccessLevel ='L4' and a.Active_Status='pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel ='L4' and a.Active_Status='pending' """)
         elif(AllowAccess =='L3' and filterDate !='All' and filterStatus =='All' and  filterUserid=='All'):
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE '{apply_filterdate}' BETWEEN start_date AND end_date and
(a.Showapprove = 0 and AccessLevel ='L4' and a.Active_Status='pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel ='L4' and a.Active_Status='pending' """)
         elif(AllowAccess =='L3' and filterUserid !='All' and filterStatus !='All' and filterDate=='All' ):
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.employeeid='{filterUserid}' and a.Active_status='{filterStatus}' and
(a.Showapprove = 0 and AccessLevel ='L4' and a.Active_Status='pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel ='L4' and a.Active_Status='pending' """)
         elif(AllowAccess =='L3' and filterUserid !='All' and filterStatus =='All' and filterDate !='All' ):
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.employeeid='{filterUserid}' and  '{apply_filterdate}' BETWEEN start_date AND end_date and
(a.Showapprove = 0 and AccessLevel ='L4' and a.Active_Status='pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel ='L4' and a.Active_Status='pending' """)
         elif(AllowAccess =='L3' and filterUserid =='All' and filterStatus !='All' and filterDate !='All' ):
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.Active_status='{filterStatus}' and  '{apply_filterdate}' BETWEEN start_date AND end_date and 
(a.Showapprove = 0 and AccessLevel ='L4' and a.Active_Status='pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel ='L4' and a.Active_Status='pending' """)
         elif(AllowAccess =='L3' and filterUserid !='All' and filterStatus !='All' and filterDate !='All' ):
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.employeeid='{filterUserid}' and a.Active_status='{filterStatus}' and  '{apply_filterdate}' BETWEEN start_date AND end_date and 
(a.Showapprove = 0 and AccessLevel ='L4' and a.Active_Status='pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel ='L4' and a.Active_Status='pending' """)
         elif(AllowAccess =='L2' and filterUserid=='All'and filterStatus =='All' and filterDate=='All'):    
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel='L3' and a.Active_Status !='L2 Accepted and L1 Pending' and a.Active_Status !='L2 Accepted' and a.Active_Status !='L1 Accepted' and a.Active_status !='L1 Rejected' and a.Active_status !='L2 Rejected' or a.Active_Status='L3 Accepted' 
ORDER BY id DESC
LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id  WHERE 
a.Showapprove = 0 and AccessLevel='L3' and a.Active_Status !='L2 Accepted' and a.Active_status !='L2 Rejected' or a.Active_Status='L3 Accepted' """)
         elif(AllowAccess =='L2'  and filterUserid !='All' and filterStatus =='All' and filterDate=='All'):    
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.employeeid='{filterUserid}' and (
a.Showapprove = 0 and AccessLevel='L3' and a.Active_Status !='L2 Accepted and L1 Pending' and a.Active_Status !='L2 Accepted' and a.Active_Status !='L1 Accepted' and a.Active_status !='L1 Rejected' and a.Active_status !='L2 Rejected' or a.Active_Status='L3 Accepted' )
ORDER BY id DESC
LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id  WHERE 
a.Showapprove = 0 and AccessLevel='L3' and a.Active_Status !='L2 Accepted' and a.Active_status !='L2 Rejected' or a.Active_Status='L3 Accepted' """)
         elif(AllowAccess =='L2'  and filterUserid =='All' and filterStatus !='All' and filterDate=='All'):    
           str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.Active_status='{filterStatus}' and (
a.Showapprove = 0 and AccessLevel='L3' and a.Active_Status !='L2 Accepted and L1 Pending' and a.Active_Status !='L2 Accepted' and a.Active_Status !='L1 Accepted' and a.Active_status !='L1 Rejected' and a.Active_status !='L2 Rejected' or a.Active_Status='L3 Accepted' )
ORDER BY id DESC
LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
           str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id  WHERE 
a.Showapprove = 0 and AccessLevel='L3' and a.Active_Status !='L2 Accepted' and a.Active_status !='L2 Rejected' or a.Active_Status='L3 Accepted' """)
         elif(AllowAccess =='L2' and filterUserid =='All' and filterStatus =='All' and filterDate !='All'):    
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE  '{apply_filterdate}' BETWEEN start_date AND end_date and
(a.Showapprove = 0 and AccessLevel='L3' and a.Active_Status !='L2 Accepted and L1 Pending' and a.Active_Status !='L2 Accepted' and a.Active_Status !='L1 Accepted' and a.Active_status !='L1 Rejected' and a.Active_status !='L2 Rejected' or a.Active_Status='L3 Accepted')
ORDER BY id DESC
LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id  WHERE 
a.Showapprove = 0 and AccessLevel='L3' and a.Active_Status !='L2 Accepted' and a.Active_status !='L2 Rejected' or a.Active_Status='L3 Accepted' """)
         elif(AllowAccess =='L2' and filterUserid!='All'and filterStatus !='All' and filterDate=='All'):    
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.employeeid='{filterUserid}' and a.Active_status='{filterStatus}' and (a.Showapprove = 0 and AccessLevel='L3' and a.Active_Status !='L2 Accepted and L1 Pending' and a.Active_Status !='L2 Accepted' and a.Active_Status !='L1 Accepted' and a.Active_status !='L1 Rejected' and a.Active_status !='L2 Rejected' or a.Active_Status='L3 Accepted') ORDER BY id DESC LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management  as a left join emp_register.employee_data as b on a.employeeid = b.id  WHERE a.Showapprove = 0 and AccessLevel='L3' and a.Active_Status !='L2 Accepted' and a.Active_status !='L2 Rejected' or a.Active_Status='L3 Accepted' """)
         elif(AllowAccess =='L2' and  filterUserid !='All' and filterStatus=='All' and filterDate!='All'):    
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.employeeid='{filterUserid}' and '{apply_filterdate}' BETWEEN start_date AND end_date and (
a.Showapprove = 0 and AccessLevel='L3' and a.Active_Status !='L2 Accepted and L1 Pending' and a.Active_Status !='L2 Accepted' and a.Active_Status !='L1 Accepted' and a.Active_status !='L1 Rejected' and a.Active_status !='L2 Rejected' or a.Active_Status='L3 Accepted' )
ORDER BY id DESC
LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id  WHERE 
a.Showapprove = 0 and AccessLevel='L3' and a.Active_Status !='L2 Accepted' and a.Active_status !='L2 Rejected' or a.Active_Status='L3 Accepted' """)
         elif(AllowAccess =='L2'  and filterUserid =='All' and filterStatus!='All' and filterDate!='None'):    
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.Active_status='{filterStatus}' and '{apply_filterdate}' BETWEEN start_date AND end_date and (a.Showapprove = 0 and AccessLevel='L3' and a.Active_Status !='L2 Accepted and L1 Pending' and a.Active_Status !='L2 Accepted' and a.Active_Status !='L1 Accepted' and a.Active_status !='L1 Rejected' and a.Active_status !='L2 Rejected' or a.Active_Status='L3 Accepted' )
           ORDER BY id DESC LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id  WHERE 
a.Showapprove = 0 and AccessLevel='L3' and a.Active_Status !='L2 Accepted' and a.Active_status !='L2 Rejected' or a.Active_Status='L3 Accepted' """)
         elif(AllowAccess =='L2'  and filterUserid !='All' and filterStatus!='All' and filterDate!='All'):    
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.employeeid='{filterUserid}' and a.Active_status='{filterStatus}' and '{apply_filterdate}' BETWEEN start_date AND end_date and
(a.Showapprove = 0 and AccessLevel='L3' and a.Active_Status !='L2 Accepted and L1 Pending' and a.Active_Status !='L2 Accepted' and a.Active_Status !='L1 Accepted' and a.Active_status !='L1 Rejected' and a.Active_status !='L2 Rejected' or a.Active_Status='L3 Accepted')
ORDER BY id DESC
LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id  WHERE 
a.Showapprove = 0 and AccessLevel='L3' and a.Active_Status !='L2 Accepted' and a.Active_status !='L2 Rejected' or a.Active_Status='L3 Accepted' """)
         elif(AllowAccess == 'L1' and filterUserid=='All'and filterStatus =='All' and filterDate=='All'):
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel='L2' and a.Active_Status='Pending' or a.Active_status='L2 Accepted and L1 Pending' ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel='L2' and a.Active_Status='Pending' or a.Active_status='L2 Accepted and L1 Pending' """)
         elif(AllowAccess == 'L1' and filterUserid !='All' and filterStatus =='All' and filterDate=='All'):
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.employeeid='{filterUserid}' and (
a.Showapprove = 0 and AccessLevel='L2' and a.Active_Status='Pending' or a.Active_status='L2 Accepted and L1 Pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel='L2' and a.Active_Status='Pending' or a.Active_status='L2 Accepted and L1 Pending' """)
         elif(AllowAccess == 'L1' and filterStatus !='All' and filterUserid =='All' and filterDate=='All'):
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.Active_status='{filterStatus}' and
(a.Showapprove = 0 and AccessLevel='L2' and a.Active_Status='Pending' or a.Active_status='L2 Accepted and L1 Pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel='L2' and a.Active_Status='Pending' or a.Active_status='L2 Accepted and L1 Pending' """)
         elif(AllowAccess == 'L1' and filterDate !='All' and filterStatus =='All' and filterUserid =='All' ):
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE  '2023-07-22' BETWEEN start_date AND end_date and (
a.Showapprove = 0 and AccessLevel='L2' and a.Active_Status='Pending' or a.Active_status='L2 Accepted and L1 Pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel='L2' and a.Active_Status='Pending' or a.Active_status='L2 Accepted and L1 Pending' """)
         elif(AllowAccess == 'L1' and filterUserid !='All'and filterStatus !='All' and filterDate!='All'):
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.employeeid='{filterUserid}' and a.Active_status='{filterStatus}' and
 '{apply_filterdate}' BETWEEN start_date AND end_date and  (a.Showapprove = 0 and AccessLevel='L2' and a.Active_Status='Pending' or a.Active_status='L2 Accepted and L1 Pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel='L2' and a.Active_Status='Pending' or a.Active_status='L2 Accepted and L1 Pending' """)
         elif(AllowAccess == 'L1' and  filterUserid !='All' and filterStatus!='All' and filterDate=='All'):
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.employeeid='{filterUserid}' and a.Active_status='{filterStatus}' and (a.Showapprove = 0 and AccessLevel='L2' and a.Active_Status='Pending' or a.Active_status='L2 Accepted and L1 Pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel='L2' and a.Active_Status='Pending' or a.Active_status='L2 Accepted and L1 Pending' """)
         elif(AllowAccess == 'L1' and  filterUserid !='All' and filterStatus=='All' and filterDate!='All'):
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.employeeid='{filterUserid}' and '{apply_filterdate}'  BETWEEN start_date AND end_date and (a.Showapprove = 0 and AccessLevel='L2' and a.Active_Status='Pending' or a.Active_status='L2 Accepted and L1 Pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel='L2' and a.Active_Status='Pending' or a.Active_status='L2 Accepted and L1 Pending' """)
         elif(AllowAccess == 'L1' and  filterUserid =='All' and filterStatus!='All' and filterDate!='All'):
          str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE  a.Active_status='{filterStatus}' and  '{apply_filterdate}'  BETWEEN start_date AND end_date and (
a.Showapprove = 0 and AccessLevel='L2' and a.Active_Status='Pending' or a.Active_status='L2 Accepted and L1 Pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
          str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel='L2' and a.Active_Status='Pending' or a.Active_status='L2 Accepted and L1 Pending' """)
           
          
         elif(AllowAccess =='L4'):     
            str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.employeeid='{id}' ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
            str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.employeeid='{id}' """)
      elif(Typesofrecords =='Process'):
         if(AllowAccess =='L3' and filterUserid=='All'and filterStatus =='All' and filterDate=='All' ):
              str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date,'%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.Active_Status='L3 Accepted' or a.Active_Status='L3 Rejected' or a.Active_status='L2 Rejected'
or a.Active_Status='L2 Accepted'  or a.Active_Status='L1 Accepted' or a.Active_status='L1 Rejected' ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
              str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.Active_Status='L3 Accepted' or a.Active_Status='L3 Rejected' or a.Active_status='L2 Rejected'
or a.Active_Status='L2 Accepted' """)
         elif(AllowAccess =='L3' and filterUserid !='All'  and filterStatus=='All' and filterDate=='All' ):
              str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date,'%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.employeeid='{filterUserid}' and (
a.Showapprove = 0 and a.Active_Status='L3 Accepted' or a.Active_Status='L3 Rejected' or a.Active_status='L2 Rejected'
or a.Active_Status='L2 Accepted'  or a.Active_Status='L1 Accepted' or a.Active_status='L1 Rejected') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
              str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.Active_Status='L3 Accepted' or a.Active_Status='L3 Rejected' or a.Active_status='L2 Rejected'
or a.Active_Status='L2 Accepted' """)
         elif(AllowAccess =='L3' and filterUserid =='All' and filterStatus!='All' and filterDate=='All'):
              str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date,'%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE  a.Active_Status='{filterStatus}' and (a.Showapprove = 0 and a.Active_Status='L3 Accepted' or a.Active_Status='L3 Rejected' or a.Active_status='L2 Rejected'
or a.Active_Status='L2 Accepted'  or a.Active_Status='L1 Accepted' or a.Active_status='L1 Rejected') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
              str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.Active_Status='L3 Accepted' or a.Active_Status='L3 Rejected' or a.Active_status='L2 Rejected'
or a.Active_Status='L2 Accepted' """)
         elif(AllowAccess =='L3' and filterUserid =='All' and filterStatus=='All' and filterDate!='All'):
              str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date,'%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE  '{apply_filterdate}'  BETWEEN start_date AND end_date and (a.Showapprove = 0 and a.Active_Status='L3 Accepted' or a.Active_Status='L3 Rejected' or a.Active_status='L2 Rejected'
or a.Active_Status='L2 Accepted'  or a.Active_Status='L1 Accepted' or a.Active_status='L1 Rejected') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
              str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.Active_Status='L3 Accepted' or a.Active_Status='L3 Rejected' or a.Active_status='L2 Rejected'
or a.Active_Status='L2 Accepted' """)
              
         if(AllowAccess =='L3' and filterUserid !='All'and filterStatus !='All' and filterDate=='All' ):
              str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date,'%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.employeeid='{filterUserid}' and a.Active_status='{filterStatus}' and (a.Showapprove = 0 and a.Active_Status='L3 Accepted' or a.Active_Status='L3 Rejected' or a.Active_status='L2 Rejected'
or a.Active_Status='L2 Accepted'  or a.Active_Status='L1 Accepted' or a.Active_status='L1 Rejected') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
              str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.Active_Status='L3 Accepted' or a.Active_Status='L3 Rejected' or a.Active_status='L2 Rejected'
or a.Active_Status='L2 Accepted' """)
         elif(AllowAccess =='L3' and  filterUserid !='All' and filterStatus=='All' and filterDate!='All' ):
              str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date,'%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.employeeid='{filterUserid}' and '{apply_filterdate}'  BETWEEN start_date AND end_date and (
a.Showapprove = 0 and a.Active_Status='L3 Accepted' or a.Active_Status='L3 Rejected' or a.Active_status='L2 Rejected'
or a.Active_Status='L2 Accepted'  or a.Active_Status='L1 Accepted' or a.Active_status='L1 Rejected') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
              str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.Active_Status='L3 Accepted' or a.Active_Status='L3 Rejected' or a.Active_status='L2 Rejected'
or a.Active_Status='L2 Accepted' """)
         elif(AllowAccess =='L3' and filterUserid =='All' and filterStatus!='All' and filterDate!='All'):
              str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date,'%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE  a.Active_Status='{filterStatus}' and '{apply_filterdate}'  BETWEEN start_date AND end_date and (a.Showapprove = 0 and a.Active_Status='L3 Accepted' or a.Active_Status='L3 Rejected' or a.Active_status='L2 Rejected'
or a.Active_Status='L2 Accepted'  or a.Active_Status='L1 Accepted' or a.Active_status='L1 Rejected') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
              str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.Active_Status='L3 Accepted' or a.Active_Status='L3 Rejected' or a.Active_status='L2 Rejected'
or a.Active_Status='L2 Accepted' """)
         elif(AllowAccess =='L3' and filterUserid !='All' and filterStatus!='All' and filterDate!='All'):
              str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date,'%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE  a.employeeid='{filterUserid}' and a.Active_status='{filterStatus}' and '{apply_filterdate}'  BETWEEN start_date AND end_date and (a.Showapprove = 0 and a.Active_Status='L3 Accepted' or a.Active_Status='L3 Rejected' or a.Active_status='L2 Rejected'
or a.Active_Status='L2 Accepted'  or a.Active_Status='L1 Accepted' or a.Active_status='L1 Rejected') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset))
              str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.Active_Status='L3 Accepted' or a.Active_Status='L3 Rejected' or a.Active_status='L2 Rejected'
or a.Active_Status='L2 Accepted' """)              
         elif(AllowAccess =='L2' and filterUserid=='All'and filterStatus =='All' and filterDate=='All' ):
            str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id  WHERE 
a.Showapprove = 0 and a.Active_Status ='L2 Rejected' or a.Active_status='L2 Accepted' or a.Active_status='L3 Rejected'  or a.Active_status='L1 Accepted' or a.Active_Status='L1 Rejected' or a.Active_status='L2 Accepted and L1 Pending' ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
            str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.Active_Status ='L2 Rejected' or a.Active_status='L2 Accepted' or a.Active_status='L3 Rejected' """)
         elif(AllowAccess =='L2' and filterUserid !='All' and filterStatus =='All' and filterDate=='All' ):
            str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id  WHERE a.employeeid='{filterUserid}' and (
a.Showapprove = 0 and a.Active_Status ='L2 Rejected' or a.Active_status='L2 Accepted' or a.Active_status='L3 Rejected'  or a.Active_status='L1 Accepted' or a.Active_Status='L1 Rejected' or a.Active_status='L2 Accepted and L1 Pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
            str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.Active_Status ='L2 Rejected' or a.Active_status='L2 Accepted' or a.Active_status='L3 Rejected' """)
         elif(AllowAccess =='L2' and filterUserid =='All' and filterStatus !='All' and filterDate=='All' ):
            str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id  WHERE a.Active_status='{filterStatus}' and (
a.Showapprove = 0 and a.Active_Status ='L2 Rejected' or a.Active_status='L2 Accepted' or a.Active_status='L3 Rejected'  or a.Active_status='L1 Accepted' or a.Active_Status='L1 Rejected' or a.Active_status='L2 Accepted and L1 Pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
            str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.Active_Status ='L2 Rejected' or a.Active_status='L2 Accepted' or a.Active_status='L3 Rejected' """)
         elif(AllowAccess =='L2' and filterUserid =='All' and filterStatus =='All' and filterDate !='All' ):
            str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id  WHERE '{apply_filterdate}'  BETWEEN start_date AND end_date and (
a.Showapprove = 0 and a.Active_Status ='L2 Rejected' or a.Active_status='L2 Accepted' or a.Active_status='L3 Rejected'  or a.Active_status='L1 Accepted' or a.Active_Status='L1 Rejected' or a.Active_status='L2 Accepted and L1 Pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
            str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.Active_Status ='L2 Rejected' or a.Active_status='L2 Accepted' or a.Active_status='L3 Rejected' """)
         elif(AllowAccess =='L2' and filterUserid !='All'and filterStatus !='All' and filterDate=='All' ):
            str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id  WHERE a.employeeid='{filterUserid}' and a.Active_status='{filterStatus}' and (a.Showapprove = 0 and a.Active_Status ='L2 Rejected' or a.Active_status='L2 Accepted' or a.Active_status='L3 Rejected'  or a.Active_status='L1 Accepted' or a.Active_Status='L1 Rejected' or a.Active_status='L2 Accepted and L1 Pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
            str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.Active_Status ='L2 Rejected' or a.Active_status='L2 Accepted' or a.Active_status='L3 Rejected' """)
         elif(AllowAccess =='L2' and filterUserid !='All' and filterStatus=='All' and filterDate!='All'):
            str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management as a left join emp_register.employee_data as b on a.employeeid = b.id  WHERE a.employeeid='{filterUserid}' and '{apply_filterdate}'  BETWEEN start_date AND end_date and  (
a.Showapprove = 0 and a.Active_Status ='L2 Rejected' or a.Active_status='L2 Accepted' or a.Active_status='L3 Rejected'  or a.Active_status='L1 Accepted' or a.Active_Status='L1 Rejected' or a.Active_status='L2 Accepted and L1 Pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
            str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.Active_Status ='L2 Rejected' or a.Active_status='L2 Accepted' or a.Active_status='L3 Rejected' """)
         elif(AllowAccess =='L2' and  filterUserid =='All' and filterStatus!='All' and filterDate!='All'):
            str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id  WHERE a.Active_status='{filterStatus}'  and '{apply_filterdate}'  BETWEEN start_date AND end_date and (
a.Showapprove = 0 and a.Active_Status ='L2 Rejected' or a.Active_status='L2 Accepted' or a.Active_status='L3 Rejected'  or a.Active_status='L1 Accepted' or a.Active_Status='L1 Rejected' or a.Active_status='L2 Accepted and L1 Pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
            str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.Active_Status ='L2 Rejected' or a.Active_status='L2 Accepted' or a.Active_status='L3 Rejected' """)
         elif(AllowAccess =='L2' and filterUserid !='All'and filterStatus !='All' and filterDate!='All'):
            str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.start_date,a.HRCmds,DATE_FORMAT(start_date, '%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date,'%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id  WHERE  a.employeeid='{filterUserid}' and a.Active_status='{filterStatus}' and '{apply_filterdate}'  BETWEEN start_date AND end_date and (
a.Showapprove = 0 and a.Active_Status ='L2 Rejected' or a.Active_status='L2 Accepted' or a.Active_status='L3 Rejected'  or a.Active_status='L1 Accepted' or a.Active_Status='L1 Rejected' or a.Active_status='L2 Accepted and L1 Pending') ORDER BY id DESC  LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )
            str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and a.Active_Status ='L2 Rejected' or a.Active_status='L2 Accepted' or a.Active_status='L3 Rejected' """)
            
         elif(AllowAccess =='L1' and filterUserid=='All'and filterStatus =='All' and filterDate=='All'):
            str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date,'%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and 
a.Active_Status='L1 Rejected' or a.Active_status='L1 Accepted' or a.Active_status='L2 Accepted' or a.Active_status='L2 Rejected'
or a.Active_status='L3 Accepted' or a.Active_status='L3 Rejected' ORDER BY id DESC LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )  
            str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and 
a.Active_Status='L1 Rejected' or a.Active_status='L1 Accepted' or a.Active_status='L2 Accepted' or a.Active_status='L2 Rejected'
or a.Active_status='L3 Accepted' or a.Active_status='L3 Rejected'""")
         elif(AllowAccess =='L1' and filterUserid !='All'and filterStatus =='All' and filterDate=='All'):
            str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date,'%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.employeeid='{filterUserid}' and (a.Showapprove = 0 and a.Active_Status='L1 Rejected' or a.Active_status='L1 Accepted' or a.Active_status='L2 Accepted' or a.Active_status='L2 Rejected' or a.Active_status='L3 Accepted' or a.Active_status='L3 Rejected') ORDER BY id DESC LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )  
            str2=(f"""SELECT COUNT(*)   from emp_register.leave_management  as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE  a.Showapprove = 0 and a.Active_Status='L1 Rejected' or a.Active_status='L1 Accepted' or a.Active_status='L2 Accepted' or a.Active_status='L2 Rejected' or a.Active_status='L3 Accepted' or a.Active_status='L3 Rejected'""")
         elif(AllowAccess =='L1' and filterUserid=='All'and filterStatus !='All' and filterDate=='All'):
            str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date,'%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
            a.Active_status='{filterStatus}' and (a.Showapprove = 0 and a.Active_Status='L1 Rejected' or a.Active_status='L1 Accepted' or a.Active_status='L2 Accepted' or a.Active_status='L2 Rejected' or a.Active_status='L3 Accepted' or a.Active_status='L3 Rejected') ORDER BY id DESC LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )  
            str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and 
a.Active_Status='L1 Rejected' or a.Active_status='L1 Accepted' or a.Active_status='L2 Accepted' or a.Active_status='L2 Rejected'
or a.Active_status='L3 Accepted' or a.Active_status='L3 Rejected'""")
         elif(AllowAccess =='L1'  and filterUserid=='All'and filterStatus =='All' and filterDate !='All'):
            str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date,'%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE '{apply_filterdate}'  BETWEEN start_date AND end_date and (
a.Showapprove = 0 and 
a.Active_Status='L1 Rejected' or a.Active_status='L1 Accepted' or a.Active_status='L2 Accepted' or a.Active_status='L2 Rejected'
or a.Active_status='L3 Accepted' or a.Active_status='L3 Rejected') ORDER BY id DESC LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )  
            str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and 
a.Active_Status='L1 Rejected' or a.Active_status='L1 Accepted' or a.Active_status='L2 Accepted' or a.Active_status='L2 Rejected'
or a.Active_status='L3 Accepted' or a.Active_status='L3 Rejected'""")
         elif(AllowAccess =='L1' and filterUserid !='All'and filterStatus !='All' and filterDate=='All'):
            str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date,'%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management  as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.employeeid='{filterUserid}' and a.Active_status='{filterStatus}' and(a.Showapprove = 0 and a.Active_Status='L1 Rejected' or a.Active_status='L1 Accepted' or a.Active_status='L2 Accepted' or a.Active_status='L2 Rejected' or a.Active_status='L3 Accepted' or a.Active_status='L3 Rejected') ORDER BY id DESC LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )  
            str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and 
a.Active_Status='L1 Rejected' or a.Active_status='L1 Accepted' or a.Active_status='L2 Accepted' or a.Active_status='L2 Rejected'
or a.Active_status='L3 Accepted' or a.Active_status='L3 Rejected'""")
         elif(AllowAccess =='L1' and filterUserid !='All' and filterStatus=='All' and filterDate!='All'):
            str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date,'%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.employeeid='{filterUserid}' and '{apply_filterdate}'  BETWEEN start_date AND end_date and(a.Showapprove = 0 and a.Active_Status='L1 Rejected' or a.Active_status='L1 Accepted' or a.Active_status='L2 Accepted' or a.Active_status='L2 Rejected' or a.Active_status='L3 Accepted' or a.Active_status='L3 Rejected') ORDER BY id DESC LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )  
            str2=(f"""SELECT COUNT(*)   from emp_register.leave_management  as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE  a.Showapprove = 0 and a.Active_Status='L1 Rejected' or a.Active_status='L1 Accepted' or a.Active_status='L2 Accepted' or a.Active_status='L2 Rejected' or a.Active_status='L3 Accepted' or a.Active_status='L3 Rejected'""")
         elif(AllowAccess =='L1' and filterUserid =='All' and filterStatus!='All' and filterDate!='All'):
            str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date,'%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel from emp_register.leave_management as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
            a.Active_status='{filterStatus}' and '{apply_filterdate}'  BETWEEN start_date AND end_date and (a.Showapprove = 0 and a.Active_Status='L1 Rejected' or a.Active_status='L1 Accepted' or a.Active_status='L2 Accepted' or a.Active_status='L2 Rejected' or a.Active_status='L3 Accepted' or a.Active_status='L3 Rejected') ORDER BY id DESC LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )  
            str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and 
a.Active_Status='L1 Rejected' or a.Active_status='L1 Accepted' or a.Active_status='L2 Accepted' or a.Active_status='L2 Rejected'
or a.Active_status='L3 Accepted' or a.Active_status='L3 Rejected'""")
         elif(AllowAccess =='L1'  and filterUserid !='All' and filterStatus!='All' and filterDate!='All'):
            str = (f"""SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.HRCmds,a.start_date,DATE_FORMAT(start_date,'%%d/%%m/%%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%%d/%%m/%%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE  a.employeeid='{filterUserid}' and a.Active_status='{filterStatus}' and '{apply_filterdate}'  BETWEEN start_date AND end_date and (
a.Showapprove = 0 and 
a.Active_Status='L1 Rejected' or a.Active_status='L1 Accepted' or a.Active_status='L2 Accepted' or a.Active_status='L2 Rejected'
or a.Active_status='L3 Accepted' or a.Active_status='L3 Rejected') ORDER BY id DESC LIMIT %s  OFFSET %s """ %(PER_PAGE, offset) )  
            str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and 
a.Active_Status='L1 Rejected' or a.Active_status='L1 Accepted' or a.Active_status='L2 Accepted' or a.Active_status='L2 Rejected'
or a.Active_status='L3 Accepted' or a.Active_status='L3 Rejected'""")
            
            
      cur.execute(str)
      listing = cur.fetchall()
      conn.commit()
      item2 = sorted(listing, key=lambda x: x['id'], reverse=True)

      cur.execute(str2)
      pagecount = cur.fetchall()

      str10 = (f"""SELECT id,firstname,lastname FROM emp_register.employee_data
      where id !='{id}'""" )
      cur.execute(str10)
      permission_userslist = cur.fetchall()
      return jsonify({'status': 200,'data':listing ,'count': pagecount[0]['COUNT(*)'],'Leavelist_userslist':permission_userslist})     
@app.route('/kpi_leave/<AllowAccess>', methods=['GET'])
def leaveKpi(AllowAccess):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor) 
    if(AllowAccess =='L3'):
        str=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel ='L4' and a.Active_Status='pending' """)
        str1=(f"""SELECT COUNT(*)   from emp_register.leave_management """)
        str2=(f"""SELECT COUNT(*)   from emp_register.leave_management """)
    elif(AllowAccess =='L2'):
        str=(f"""SELECT COUNT(*)   from emp_register.leave_management 
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel='L3' and a.Active_Status !='L2 Accepted and L1 Pending' and a.Active_Status !='L2 Accepted' and a.Active_status !='L1 Rejected' and a.Active_status !='L2 Rejected' or a.Active_Status='L3 Accepted' 
 """)
        str1=(f"""SELECT COUNT(*) from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id  WHERE 
a.Showapprove = 0 and a.Active_Status ='L2 Rejected' or a.Active_status='L2 Accepted' or a.Active_status='L3 Rejected'  or a.Active_status='L1 Accepted' or a.Active_Status='L1 Rejected' or a.Active_status='L2 Accepted and L1 Pending' """)
        str2=(f"""SELECT COUNT(*)   from emp_register.leave_management """)
    elif(AllowAccess =='L1'):
        str=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and AccessLevel='L2' and a.Active_Status='Pending'""")
        str1=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and 
a.Active_Status='L1 Rejected' or a.Active_status='L1 Accepted' or a.Active_status='L2 Accepted' or a.Active_status='L2 Rejected'
or a.Active_status='L3 Accepted' or a.Active_status='L3 Rejected' 
 """)   
        str2=(f"""SELECT COUNT(*)   from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.Showapprove = 0 and  a.Active_status='L2 Accepted and L1 Pending' """)
        
    
       
    cur.execute(str)
    total_pending = cur.fetchall()

    cur.execute(str1)
    Reqpending= cur.fetchall()

    cur.execute(str2)
    Passtoreq = cur.fetchall()

   
    return jsonify({'status': 200,'count': total_pending[0]['COUNT(*)'],'Request': Reqpending[0]['COUNT(*)'],'passtol1': Passtoreq[0]['COUNT(*)']})
  
@app.route('/viewPermission/<id>', methods=['GET'])
def viewPermission(id):

    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'GET':
        str1 = (f"""
                SELECT a.id,a.employeeid,a.leave_type,a.Active_status,a.start_date,a.Leadcmds,a.Headcmds,a.start_date,a.HRCmds,DATE_FORMAT(start_date, "%M %d, %Y") AS firstday,a.end_date,DATE_FORMAT(end_date,"%M %d, %Y") AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id 
WHERE a.Showapprove = 0  and   a.id='{id}'""")
        cur.execute(str1)
        data = cur.fetchall()
      
        conn.commit()
        return jsonify({'data': data})
@app.route('/viewTickets/<id>', methods=['GET'])
def viewTickets(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'GET':
        str1 = (f"""SELECT * from emp_register.ticketrise_table as a left join emp_register.employee_data as b on b.id = a.To_Email where a.id='{id}'""")        
        cur.execute(str1)
        data = cur.fetchall()
        conn.commit()
        str2= (f"""SELECT  a.ticketid, a.userid, a.CC_Emails, b.id, b.firstname, b.lastname, b.email, b.mobileno, b.country, b.city, b.password, b.gender, b.Approved, b.profile, b.Active_Status, b.forgotpassword, b.AccessLevel, b.employeeId, b.Emp_level  from emp_register.ccemail_data   
as a left join emp_register.employee_data as b on b.id = a.CC_Emails where ticketid='{id}'""")
        cur.execute(str2)
        data_ccemail = cur.fetchall()
       
        conn.commit()
        return jsonify({'data': data,'ccemail': data_ccemail})    
   
@app.route('/emplyeedel/<id>', methods=['DELETE'])
def Employee_deleted(id):
   
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    str = f"""update leave_management set Showapprove=1 WHERE id='{id}';"""

    cur.execute(str)
    conn.commit()
    return jsonify({'status': 200, 'msg': 'Deleted Successfully!'})
@app.route('/leaveUpdate/<id>', methods=['PUT'])
def leaveUpdate(id):
   
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    data = request.json

    str = f"""update leave_management set leave_type='{data["Leave Type"]}',start_date='{data['Fromdate']}',end_date='{data['ToDate']}',comments='{data["comments"]}' WHERE id={id};"""

    cur.execute(str)
    conn.commit()
   
  
    return jsonify({'status': 200, 'msg': 'Updated Successfull!'})
@app.route('/AcceptUpdate/<id>', methods=['PUT'])
def AcceptUpdate(id):

    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    data = request.json
 
    updateStatus=data['AcceptUpdate']

    Notification_Process=data['Notification_process']
    employee_name=data['Employee_name']
    approvedTiming=data['Accept_Time']
    levelof_user=data['levelof_emp']
    UsersId=data['UserId']
    Process_result=updateStatus
    Req_emp=data['Request_emplevel']

    Subject='Leave Request'
    sender_email=data['Sender_email']
   
    leave_type=data['Leavetype']
    end_Date=data['Leave_end']
    start_date=data['Leave_start']

    input_format = "%a, %d %b %Y %H:%M:%S %Z"
    output_format = "%B %d, %Y"
    date_object = datetime.strptime(start_date, input_format)
    Start_formatted_date = date_object.strftime(output_format)
  
    date_object1= datetime.strptime(end_Date, input_format)
    enddate_formatted_date = date_object1.strftime(output_format)

   
    AccessLevel_emp=data['levelof_emp']
    if(levelof_user=='L3' and Process_result=='L3 Accepted' and 
        Req_emp=='L4' ):
        Levelof_email='L2'
        check_process= f"""SELECT id FROM emp_register.employee_data
where AccessLevel='{Levelof_email}'"""
        cur.execute(check_process)
        GetSend_id = cur.fetchall()
        arrayof_id = [item['id'] for item in GetSend_id]
        Send_email = str(arrayof_id)[1:-1]
     
    elif(levelof_user=='L3' and Process_result =='L3 Rejected' and Req_emp=='L4'):
        Levelof_email=id
        check_process= f"""SELECT b.id from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id 
WHERE a.Showapprove = 0  and   a.id={Levelof_email}"""
        cur.execute(check_process)
        GetSend_id = cur.fetchall()
        arrayof_id = [item['id'] for item in GetSend_id]
        Send_email = str(arrayof_id)[1:-1]

    elif(levelof_user=='L2' and Process_result =='L2 Accepted' and Req_emp=='L4'):
        Levelof_email=id
        check_process= f"""SELECT b.id from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id 
WHERE a.Showapprove = 0  and   a.id={Levelof_email}"""
        cur.execute(check_process)
        GetSend_id = cur.fetchall()
        arrayof_id = [item['id'] for item in GetSend_id]
        Send_email = str(arrayof_id)[1:-1]

    elif(levelof_user=='L2' and Process_result =='L2 Accepted' and Req_emp=='L3'):
        Levelof_email=id
        check_process= f"""SELECT b.id from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id 
WHERE a.Showapprove = 0  and   a.id={Levelof_email}"""
        cur.execute(check_process)
        GetSend_id = cur.fetchall()
        arrayof_id = [item['id'] for item in GetSend_id]
        Send_email = str(arrayof_id)[1:-1]

    elif(levelof_user=='L2' and Process_result =='L2 Rejected'  and Req_emp=='L4'):
        Levelof_email=id
        check_process= f"""SELECT b.id from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id 
WHERE a.Showapprove = 0  and   a.id={Levelof_email}"""
        cur.execute(check_process)
        GetSend_id = cur.fetchall()
        arrayof_id = [item['id'] for item in GetSend_id]
        Send_email = str(arrayof_id)[1:-1]

    elif(levelof_user=='L2' and Process_result =='L2 Rejected'  and Req_emp=='L3'):
        Send_email=id   
    elif(levelof_user=='L2' and Process_result =='L2 Accepted and L1 Pending' and Req_emp=='L4'):
        Levelof_email='L1'
        check_process= f"""SELECT id FROM emp_register.employee_data
where AccessLevel='{Levelof_email}'"""
        cur.execute(check_process)
        GetSend_id = cur.fetchall()
        arrayof_id = [item['id'] for item in GetSend_id]
        Send_email = str(arrayof_id)[1:-1]
 
    elif(levelof_user=='L2' and Process_result =='L2 Accepted and L1 Pending' and Req_emp=='L3'):
        Levelof_email='L1'
        check_process= f"""SELECT id FROM emp_register.employee_data
where AccessLevel='{Levelof_email}'"""
        cur.execute(check_process)
        GetSend_id = cur.fetchall()
        arrayof_id = [item['id'] for item in GetSend_id]
        Send_email = str(arrayof_id)[1:-1]

    elif(levelof_user=='L1' and Process_result =='L1 Accepted' and Req_emp=='L4'):
        Levelof_email=id
        check_process= f"""SELECT b.id from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id 
WHERE a.Showapprove = 0  and   a.id={Levelof_email}"""
        cur.execute(check_process)
        GetSend_id = cur.fetchall()
        arrayof_id = [item['id'] for item in GetSend_id]
        Send_email = str(arrayof_id)[1:-1]

        
    elif(levelof_user=='L1' and Process_result =='L1 Accepted' and Req_emp=='L3'):
        Levelof_email=id
        check_process= f"""SELECT b.id from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id 
WHERE a.Showapprove = 0  and   a.id={Levelof_email}"""
        cur.execute(check_process)
        GetSend_id = cur.fetchall()
        arrayof_id = [item['id'] for item in GetSend_id]
        Send_email = str(arrayof_id)[1:-1]

    elif(levelof_user=='L1' and Process_result =='L1 Accepted' and Req_emp=='L2'):
        Levelof_email=id
        check_process= f"""SELECT b.id from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id 
WHERE a.Showapprove = 0  and   a.id={Levelof_email}"""
        cur.execute(check_process)
        GetSend_id = cur.fetchall()
        arrayof_id = [item['id'] for item in GetSend_id]
        Send_email = str(arrayof_id)[1:-1]
    
    elif(levelof_user=='L1' and Process_result =='L1 Rejected' and Req_emp=='L4' ):
        Levelof_email=id
        check_process= f"""SELECT b.id from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id 
WHERE a.Showapprove = 0  and   a.id={Levelof_email}"""
        cur.execute(check_process)
        GetSend_id = cur.fetchall()
        arrayof_id = [item['id'] for item in GetSend_id]
        Send_email = str(arrayof_id)[1:-1]

    elif(levelof_user=='L1' and Process_result =='L1 Rejected' and Req_emp=='L3'):
        Levelof_email=id
        check_process= f"""SELECT b.id from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id 
WHERE a.Showapprove = 0  and   a.id={Levelof_email}"""
        cur.execute(check_process)
        GetSend_id = cur.fetchall()
        arrayof_id = [item['id'] for item in GetSend_id]
        Send_email = str(arrayof_id)[1:-1]

    elif(levelof_user=='L1' and Process_result =='L1 Rejected' and Req_emp=='L2'):
        Levelof_email=id
        check_process= f"""SELECT b.id from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id 
WHERE a.Showapprove = 0  and   a.id={Levelof_email}"""
        cur.execute(check_process)
        GetSend_id = cur.fetchall()
        arrayof_id = [item['id'] for item in GetSend_id]
        Send_email = str(arrayof_id)[1:-1]
   
    
    # cur.execute(Send_email)
    # SendLead = cur.fetchall()

    Send_email2=Send_email

    sender_id=data['sender_id']
    profile_mainid=data['profilemainid']

#     str1=f"""SELECT email,firstname,id FROM emp_register.employee_data
# where AccessLevel='{Send_email2}'"""
#     # str1=f""" SELECT b.id,b.firstname,b.email from emp_register.leave_management as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE a.Showapprove = 0  and   a.id='{id}'"""

#     cur.execute(str1)
#     SendLead = cur.fetchall()

    # SendTeamLead_values = [item['id'] for item in SendLead]


    RequestTo=Send_email
    if(AccessLevel_emp == 'L3'):
         Teamlead_cmds=data['teamlead_comments']
         if(Teamlead_cmds !=None):
            Teamlead_cmds=Teamlead_cmds
         else:
            Teamlead_cmds='none' 
         str6 = f"""update leave_management set Active_status='{updateStatus}', Leadcmds='{Teamlead_cmds}' ,Approved_Timing='{approvedTiming}'  WHERE id={id};"""
         str7=f"""SELECT id,email,firstname FROM emp_register.employee_data where id='{RequestTo}';"""
         cur.execute(str7)
         SendTeamLead = cur.fetchall()
         SendTeamLead_values = [item['id'] for item in SendTeamLead]

         email_values = [d['email'] for d in SendTeamLead] 

         teamLeads_names = [d['firstname'] for d in SendTeamLead]

         result_leadsName = ''.join(teamLeads_names)

         for user,message, team_lead_name in zip(SendTeamLead_values,email_values, teamLeads_names):
            AddRow1=f"""INSERT INTO notification_data(message, notification_type, pageId, request_from, request_to) VALUES('{Notification_Process}','{data['Notification_type']}','{data['ShowpageId']}','{AccessLevel_emp}','{RequestTo}');"""

            cur.execute(AddRow1)
            cur.fetchall()
            conn.commit()
            user_email=message
            msg = Message(Subject,sender=sender_email, recipients=[user_email])
            msg.html = render_template('LeaveReqTemp.html',Team_leads=team_lead_name,ViewpageId=id,teamLeads_names=result_leadsName,Employee_name=employee_name,Levelof_Emp=Process_result,Leave_Type=leave_type,Starting_lev=Start_formatted_date,ending_lev=enddate_formatted_date)
            mail.send(msg)    
   



            
    elif(AccessLevel_emp =='L2'):
        HrComments=data['Hr_comments']
        if(HrComments !=None):
            HrComments=HrComments
        else:
            HrComments='none'    
        str6 = f"""update leave_management set Active_status='{updateStatus}',HRCmds='{HrComments}',Approved_Timing='{approvedTiming}'  WHERE id={id};"""
        
        str7=f"""SELECT id,email,firstname FROM emp_register.employee_data where id='{RequestTo}';"""
        cur.execute(str7)
        SendTeamLead = cur.fetchall()
        SendTeamLead_values = [item['id'] for item in SendTeamLead]

        email_values = [d['email'] for d in SendTeamLead] 
  
        teamLeads_names = [d['firstname'] for d in SendTeamLead]

        result_leadsName = ''.join(teamLeads_names)
  
        for user,message, team_lead_name in zip(SendTeamLead_values,email_values, teamLeads_names):
            AddRow1=f"""INSERT INTO notification_data(message, notification_type, pageId, request_from, request_to) VALUES('{Notification_Process}','{data['Notification_type']}','{data['ShowpageId']}','{AccessLevel_emp}','{RequestTo}');"""
    
            cur.execute(AddRow1)
            cur.fetchall()
            conn.commit()
            user_email=message
            msg = Message(Subject,sender=sender_email, recipients=[user_email])
            msg.html = render_template('LeaveReqTemp.html',Team_leads=team_lead_name,ViewpageId=id,teamLeads_names=result_leadsName,Employee_name=employee_name,Levelof_Emp=Process_result,Leave_Type=leave_type,Starting_lev=Start_formatted_date,ending_lev=enddate_formatted_date)
            mail.send(msg)
    elif(AccessLevel_emp == 'L1'):
         headof_cmds=data['head_comments']
         if(headof_cmds !=None):
            headof_cmds=headof_cmds
         else:
            headof_cmds='none' 
  
         str6 = f"""update leave_management set Active_status='{updateStatus}',Headcmds='{headof_cmds}',Approved_Timing='{approvedTiming}'    WHERE id={id};"""
        
        
         str7=f"""SELECT id,email,firstname FROM emp_register.employee_data where id='{RequestTo}';"""
         cur.execute(str7)
         SendTeamLead = cur.fetchall()
         SendTeamLead_values = [item['id'] for item in SendTeamLead]

         email_values = [d['email'] for d in SendTeamLead] 
  
         teamLeads_names = [d['firstname'] for d in SendTeamLead]

         result_leadsName = ''.join(teamLeads_names)
 
         for user,message, team_lead_name in zip(SendTeamLead_values,email_values, teamLeads_names):
            AddRow1=f"""INSERT INTO notification_data(message, notification_type, pageId, request_from, request_to) VALUES('{Notification_Process}','{data['Notification_type']}','{data['ShowpageId']}','{AccessLevel_emp}','{RequestTo}');"""
  
            cur.execute(AddRow1)
            cur.fetchall()
            conn.commit()
            user_email=message
            msg = Message(Subject,sender=sender_email, recipients=[user_email])
            msg.html = render_template('LeaveReqTemp.html',Team_leads=team_lead_name,ViewpageId=id,teamLeads_names=result_leadsName,Employee_name=employee_name,Levelof_Emp=Process_result,Leave_Type=leave_type,Starting_lev=Start_formatted_date,ending_lev=enddate_formatted_date)
            mail.send(msg)
          

    cur.execute(str6)
    conn.commit()
   

    # email_values = [d['email'] for d in SendLead] 
 
    # teamLeads_names = [d['firstname'] for d in SendLead]

    #     # result_leadsName = ''.join(teamLeads_names)

    # if(email_values == []):
    #     str2=f"""SELECT email,firstname FROM emp_register.employee_data
    #  where AccessLevel='{Send_email}' """
    #     cur.execute(str2)
    #     Sendnextlevel = cur.fetchall()

    #     email_values = [d['email'] for d in Sendnextlevel]
    #     teamLeads_names = [d['firstname'] for d in Sendnextlevel]

    #     result_leadsName = ''.join(teamLeads_names)

    # else:
    #     email_values=email_values
    #     teamLeads_names=teamLeads_names
    #     result_leadsName = ''.join(teamLeads_names)

            
    # for message, team_lead_name in zip(email_values, teamLeads_names):
    #         user_email=message
    #         msg = Message(Subject,sender=sender_email, recipients=[user_email])
    #         msg.html = render_template('LeaveReqTemp.html',Team_leads=team_lead_name,ViewpageId=id,teamLeads_names=result_leadsName,Employee_name=employee_name,Levelof_Emp=Process_result,Leave_Type=leave_type,Starting_lev=Start_formatted_date,ending_lev=enddate_formatted_date)
    # #         mail.send(msg)
    return jsonify({'status': 200, 'msg': 'Updated Successfull!'})















@app.route('/viewleaveReqpage/<empid>', methods=['GET'])
def viewLeavepage_details(empid):

    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    # str1 = (f"""select * From  leave_management  where empid='{empid}'""")
    str1 = (f"""SELECT a.id,a.employeeid,a.leave_type,a.start_date,a.Active_status,a.start_date,DATE_FORMAT(start_date, '%d/%m/%Y') AS firstday,a.end_date,DATE_FORMAT(end_date, '%d/%m/%Y') AS lastday,a.comments,b.firstname,b.lastname ,b.email,b.mobileno,b.AccessLevel
from emp_register.leave_management   
as a left join emp_register.employee_data as b on a.employeeid = b.id WHERE 
a.id='{empid}'""" )
    cur.execute(str1)
    data = cur.fetchall()

    conn.commit()
    return jsonify({'data': data}) 

@app.route('/TicketRise_listing/<tab>', methods=['POST'])
def TicketRise_listing(tab):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    data = request.json

    Profileid=data['employeeId']
    label=data['tab_label']
    filter_user=data['filter_user']
    filter_status=data['filter_status']
    str2 = (f"""SELECT email FROM emp_register.employee_data
where id='{Profileid}'""" )
    cur.execute(str2)
    current_user = cur.fetchall()
    currentuser_email = current_user[0]['email']
    str10 = (f"""SELECT id,firstname,lastname FROM emp_register.employee_data
where id !='{Profileid}'""" )
    cur.execute(str10)
    OverAllusers_dropdown = cur.fetchall()
    if(label =='Own'):
        
        if filter_user == 'All' and filter_status=='All':
            str1 = (f"""SELECT *  from emp_register.ticketrise_table   
as a left join emp_register.employee_data as b on b.id = a.To_Email
where user_id='{Profileid}' """)
        elif filter_user == 'All' and filter_status !='All':
            str1 = (f"""SELECT *  from emp_register.ticketrise_table   
as a left join emp_register.employee_data as b on b.id = a.To_Email
where user_id='{Profileid}' and status='{filter_status}' """ )
        elif filter_user != 'All' and filter_status=='All':
            str1 = (f"""SELECT a.id, MAX(a.user_id) AS user_id, MAX(a.To_Email) AS To_Email,    MAX(a.Subject) AS Subject,
    MAX(a.Message) AS Message,
    MAX(a.status) AS status,
	MAX(b.id) AS id,
    MAX(b.ticketid) AS ticketid,
	MAX(b.userid) AS userid,
    MAX(b.CC_Emails) AS CC_Emails,
	MAX(c.firstname) AS firstname,
    MAX(c.lastname) AS lastname
FROM emp_register.ticketrise_table AS a
LEFT JOIN emp_register.ccemail_data AS b ON b.userid = a.user_id
LEFT JOIN emp_register.employee_data AS c ON c.id = a.user_id
where c.id='{Profileid}' and (a.To_Email='{filter_user}' or b.CC_Emails='{filter_user}')
group by a.id""")
        elif filter_user != 'All' and filter_status !='All':
            str1 = (f"""SELECT a.id, MAX(a.user_id) AS user_id, MAX(a.To_Email) AS To_Email,    MAX(a.Subject) AS Subject,
    MAX(a.Message) AS Message,
    MAX(a.status) AS status,
	MAX(b.id) AS id,
    MAX(b.ticketid) AS ticketid,
	MAX(b.userid) AS userid,
    MAX(b.CC_Emails) AS CC_Emails,
	MAX(c.firstname) AS firstname,
    MAX(c.lastname) AS lastname
FROM emp_register.ticketrise_table AS a
LEFT JOIN emp_register.ccemail_data AS b ON b.userid = a.user_id
LEFT JOIN emp_register.employee_data AS c ON c.id = a.user_id
where c.id='{filter_user}' and (a.status='{filter_status}' and a.To_Email='{Profileid}' or b.CC_Emails='{Profileid}')
group by a.id""")
        
    else: 

        if filter_user == 'All' and filter_status=='All':
            str1 = (f"""SELECT a.id, MAX(a.user_id) AS user_id, MAX(a.To_Email) AS To_Email,    MAX(a.Subject) AS Subject,MAX(a.Message) AS Message,MAX(a.status) AS status,MAX(b.id) AS id,MAX(b.ticketid) AS ticketid,MAX(b.userid) AS userid,MAX(b.CC_Emails) AS CC_Emails,MAX(c.firstname) AS firstname,MAX(c.lastname) AS lastname
            FROM emp_register.ticketrise_table AS a
            LEFT JOIN emp_register.ccemail_data AS b ON b.userid = a.user_id
            LEFT JOIN emp_register.employee_data AS c ON c.id = a.user_id
            WHERE a.To_Email = '{Profileid}' OR b.CC_Emails = '{Profileid}'
            GROUP BY a.id""")
        elif filter_user == 'All' and filter_status !='All':
            str1 = (f"""SELECT a.id, MAX(a.user_id) AS user_id, MAX(a.To_Email) AS To_Email,    MAX(a.Subject) AS Subject,MAX(a.Message) AS Message,MAX(a.status) AS status,MAX(b.id) AS id,MAX(b.ticketid) AS ticketid,MAX(b.userid) AS userid,MAX(b.CC_Emails) AS CC_Emails,MAX(c.firstname) AS firstname,MAX(c.lastname) AS lastname
            FROM emp_register.ticketrise_table AS a
            LEFT JOIN emp_register.ccemail_data AS b ON b.userid = a.user_id
            LEFT JOIN emp_register.employee_data AS c ON c.id = a.user_id
            WHERE a.status='{filter_status}' and (a.To_Email = '{Profileid}' OR b.CC_Emails = '{Profileid}') 
            GROUP BY a.id""")
        elif filter_user != 'All' and filter_status=='All':
            str1 = (f"""SELECT a.id, MAX(a.user_id) AS user_id, MAX(a.To_Email) AS To_Email,    MAX(a.Subject) AS Subject,MAX(a.Message) AS Message,MAX(a.status) AS status,MAX(b.id) AS id,MAX(b.ticketid) AS ticketid,MAX(b.userid) AS userid,MAX(b.CC_Emails) AS CC_Emails,MAX(c.firstname) AS firstname,MAX(c.lastname) AS lastname
            FROM emp_register.ticketrise_table AS a
            LEFT JOIN emp_register.ccemail_data AS b ON b.userid = a.user_id
            LEFT JOIN emp_register.employee_data AS c ON c.id = a.user_id
            WHERE  c.id='{filter_user}' and (a.To_Email = '{Profileid}' OR b.CC_Emails = '{Profileid}')  
            GROUP BY a.id""")
        elif filter_user != 'All' and filter_status !='All':
            str1 = (f"""SELECT a.id, MAX(a.user_id) AS user_id, MAX(a.To_Email) AS To_Email,    MAX(a.Subject) AS Subject,MAX(a.Message) AS Message,MAX(a.status) AS status,MAX(b.id) AS id,MAX(b.ticketid) AS ticketid,MAX(b.userid) AS userid,MAX(b.CC_Emails) AS CC_Emails,MAX(c.firstname) AS firstname,MAX(c.lastname) AS lastname
            FROM emp_register.ticketrise_table AS a
            LEFT JOIN emp_register.ccemail_data AS b ON b.userid = a.user_id
            LEFT JOIN emp_register.employee_data AS c ON c.id = a.user_id
            WHERE c.id='{filter_user}' and a.status='{filter_status}' and (a.To_Email = '{Profileid}' OR b.CC_Emails ='{Profileid}')
            GROUP BY a.id """)
    cur.execute(str1)
    data = cur.fetchall()

    conn.commit()

    
    return jsonify({'data': data,'allDrpdown_users':OverAllusers_dropdown})      


@app.route('/ShowUsers_ticket', methods=['POST', 'GET'])
def ShowUsers_ticket():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json

        To_Email=data['to']

        CC_Email=data['cc']

        int_Toemails = list([To_Email])

        Sender_Emailid=data['ProfileEmailid']
        sender_email='vijaysethu0101@gmail.com'
        formatted_CCemails = str(CC_Email).strip('[]')

        Subject=data['subject']
        Messages=data['message']
        Profileid=data['Profileid']
        Notification_type=data['Notification_type']
        id = uuid.uuid1()
        userid=id.hex
        str1=(f"""INSERT INTO ticketrise_table(id, user_id, To_Email, Subject, Message) VALUES('{userid}','{Profileid}','{To_Email}','{Subject}','{Messages}'); """)
        cur.execute(str1)
        str3 =(f"""INSERT INTO ccemail_data(ticketid, userid, CC_Emails)VALUES( %s, %s, %s)""")
        for cc_email in CC_Email:
            values = (userid, Profileid, cc_email)
            cur.execute(str3, values)
        conn.commit()    
        CC_emailsId=int_Toemails+CC_Email

        str15 = (f"""SELECT firstname FROM emp_register.employee_data WHERE id='{Profileid}' ;""")
        cur.execute(str15)
        datanotifi = cur.fetchall()

        usernameof_notification=datanotifi[0]['firstname']
        Notification_text='Ticket Raised by'
        concatenated_notification = f'{Notification_text} {usernameof_notification}'
        for user in CC_emailsId:
             str5=f"""INSERT INTO notification_data(message, notification_type, pageId, request_from, request_to) VALUES('{concatenated_notification}','{Notification_type}','{userid}','{Profileid}','{user}'); """
             cur.execute(str5)
             cur.fetchall()
             conn.commit()
        str2 = (f"""SELECT email,firstname FROM emp_register.employee_data
        where id='{To_Email}' """)
        cur.execute(str2)

        current_To = cur.fetchall()
        ToUser_Email=current_To[0]['email']
        ToUserName=current_To[0]['firstname']

        CC = []
        for CC_id in CC_Email:
            str7= (f"""SELECT email,firstname FROM emp_register.employee_data
            where id='{CC_id}' """)
            cur.execute(str7)
            current_CC = cur.fetchall()
            CCUser_Email=current_CC[0]['email']
            CCUser_name=current_CC[0]['firstname']

            CC.append(CCUser_Email)  
  
        msg = Message(Subject,sender=Sender_Emailid, recipients=[ToUser_Email],cc=CC)
        msg.html = render_template('Ticket_emailtemp.html',Team_leads='Vijay',ViewUserid=userid,To_email=ToUserName,CC_email=CCUser_name,Subject=Subject,Message=Messages)
        mail.send(msg)
        return jsonify({'status': 200, 'message': 'Email Send Successfull!'})
    else:
        str1 = "SELECT * FROM employee_data where Approved='0' order by AccessLevel"
        cur.execute(str1)
        ShowUsers = cur.fetchall()

        return jsonify({'data':ShowUsers})
@app.route('/TicketReply_update/<id>', methods=['PUT'])
def TicketReply_update(id):

    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    data = request.json
  
    update_reply=data['reply_status']   
    To_emails=data['To_Emails']  

    CC_Emails=data['CC_Emails']
    Subject=data['Subject']
    ReqSend_users=data['userid']

    Sender_Emailid='vijaysethu0101@gmail.com'
    updatenotifi_text=' Your Raised Ticket Has Been Resolved'
    notification_type='Ticket Raising'
    CC=[]
    CC_emailsStr=str(CC_Emails)
    for CC_emailid in CC_Emails:
        str1 = "SELECT email FROM employee_data where id='" + str(CC_emailid) + "'"
        cur.execute(str1)
        ToEmailid = cur.fetchall()

        ToemailIds=ToEmailid[0]['email']
        CC.append(ToemailIds)  

    updateReply_status='Completed'
    str9 = f"""update emp_register.ticketrise_table set status='{updateReply_status}'  WHERE id='{id}'""" 
    cur.execute(str9)
    conn.commit()
    str5=f"""INSERT INTO notification_data(message, notification_type, pageId, request_from, request_to) VALUES('{updatenotifi_text}','{notification_type}','{id}','{To_emails}','{ReqSend_users}'); """
    cur.execute(str5)
    cur.fetchall()
    conn.commit()
    str6 = "SELECT email FROM employee_data where id=%s"
    cur.execute(str6,ReqSend_users)
    replyemailids = cur.fetchall()

    replyemailid=replyemailids[0]['email']
    
    msg = Message(Subject,sender=To_emails, recipients=[replyemailid],cc=CC)
    msg.html = render_template('Ticket_emailtemp.html',ViewUserid=id,To_email=To_emails,CC_email=CC,Subject=Subject,Message=update_reply)
    mail.send(msg)
    return jsonify({'status': 200, 'msg': 'Updated Successfully!'})
def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    formatted_str = f"{hours}:{minutes:02d}:{seconds:02d}"
    return formatted_str
def calculate_time_difference(time_in, time_out):
    time_format = "%H:%M:%S"
    time_in_obj = datetime.strptime(time_in, time_format)
    time_out_obj = datetime.strptime(time_out, time_format)
    time_difference = time_out_obj - time_in_obj
    return time_difference



@app.route('/Attend_dailyEntry', methods=['POST', 'GET'])
def Attend_dailyEntry():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json

        profile_id = data['Profileid']
        timeIn = data['time']
        entryDate=data['date']
        entryType=data['type']
        if(entryType =='In'):
            Status_val=1
        else:
            Status_val=0    
        str1=f"""INSERT INTO daily_attendanceentry(userid, date, timeIn,status) VALUES('{profile_id}','{entryDate}','{timeIn}','{Status_val}'); """
        cur.execute(str1)
        cur.fetchall()
        conn.commit()
        totalTime='00:10:00'
        if(entryType =='Out'):
            str4 = "SELECT timeIn FROM daily_attendanceentry where userid='"+profile_id+"' and status='1' order by id desc limit 1"
            cur.execute(str4)
            showTimein = cur.fetchall()

            time_in_value = showTimein[0]['timeIn']
            formatted_time_in = str(time_in_value)
            formatted_time = format_timedelta(time_in_value)
        else:
            formatted_time='00:00:00'
                
      
          
        
        diff = calculate_time_difference(formatted_time, timeIn)
        initialEntry='00:00:00'
        str7 = "SELECT * FROM daily_mainentry where userid='"+profile_id+"' and date='"+entryDate+"'"
        cur.execute(str7)
        checkEMpentry = cur.fetchall()
  
        if(checkEMpentry !=() and entryType =='Out'):
            str9 = "SELECT totalTime FROM daily_mainentry where userid='"+profile_id+"' and date='"+entryDate+"'"
            cur.execute(str9)
            querygetValue= cur.fetchall()
            previousEntry=querygetValue[0]['totalTime']

            previousEntry_str = str(previousEntry)
            diff_str = str(diff)
            time_format = "%H:%M:%S"
            datetime_obj_1 = datetime.strptime(previousEntry_str, time_format)
            datetime_obj_2 = datetime.strptime(diff_str, time_format)
            sum_datetime = datetime_obj_1 + timedelta(seconds=datetime_obj_2.hour*3600 + datetime_obj_2.minute*60 + datetime_obj_2.second)
            sum_time = sum_datetime.strftime(time_format)
            str8 = f"""update emp_register.daily_mainentry set totalTime='{sum_time}'  WHERE userid='{profile_id}' and date='{entryDate}';
;""" 
            cur.execute(str8)
            conn.commit()
        elif(checkEMpentry !=() and entryType =='In'):  
            updateIn_status='1'
            str9 = f"""update emp_register.daily_mainentry set status='{updateIn_status}'  WHERE userid='{profile_id}' and date='{entryDate}';""" 
            cur.execute(str9)
            conn.commit()

        return jsonify({'status': 200, 'message': 'Daily Entry Successfull!'})
    
    
@app.route('/main_AttendEntry', methods=['POST', 'GET'])
def main_AttendEntry():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json
    
        str1 = "SELECT id FROM emp_register.employee_data where Active_Status='True'"
        cur.execute(str1)
        OverallUsers = cur.fetchall()
 
        activeusers_id = [item['id'] for item in OverallUsers]

        profile_id = data['Profileid']
        timeIn = data['time']

        entryDate=data['date']
        today_date = datetime.strptime(entryDate, '%Y-%m-%d').date()
        previous_date = today_date - timedelta(days=1)

        totalDuration=data['Totaltime']
        for user_id in activeusers_id:
            str5 = "SELECT COUNT(*) FROM emp_register.daily_attendanceentry where date=%s and userid=%s "
            check_Outentry=(previous_date,user_id)
            cur.execute(str5,check_Outentry)
            check_Outentrys = cur.fetchall()
            count_value = check_Outentrys[0]['COUNT(*)']
            if count_value % 2 == 0:
                result_lastentry='even'
            else:
                result_lastentry='odd'

            logout_time='18:00:00'
            update_entroutStatus='0'
            if(result_lastentry =='odd'):
                str7 = "SELECT timeIn FROM emp_register.daily_attendanceentry where date=%s and userid=%s order by id desc limit 1 "
                lastEntry_timeIn=(previous_date,user_id)
                cur.execute(str7,lastEntry_timeIn)
                getlastEntry_timeIn = cur.fetchall()
                lastEntry_time = getlastEntry_timeIn[0]['timeIn']
                minutes_to_add = 2
                reference_time = datetime.strptime('00:00:00', '%H:%M:%S').replace(hour=0, minute=0, second=0)
                new_time = reference_time + lastEntry_time + timedelta(minutes=minutes_to_add)
                new_time_str = new_time.strftime('%H:%M:%S')
          
                str6 =(f"""INSERT INTO daily_attendanceentry(userid, date, timeIn, status)VALUES(%s, %s,%s, %s)""")
                values = (user_id, previous_date,new_time_str,update_entroutStatus)
                cur.execute(str6,values)
                conn.commit()
                
            
            
        for user_id in activeusers_id:
            str2 = "SELECT * FROM emp_register.daily_mainentry where date=%s and userid=%s "
            value_pass=(entryDate,user_id)
            cur.execute(str2,value_pass)
            check_OverallUsers = cur.fetchall()
            
                   
        if(check_OverallUsers ==()):
            for Empid in activeusers_id:
                str10 = "SELECT * FROM emp_register.leave_management WHERE %s BETWEEN start_date AND end_date and employeeid=%s AND (Active_status = 'L2 Accepted' OR Active_status = 'L1 Accepted')"
                passed_values=(entryDate,Empid)
                cur.execute(str10,passed_values)
                updateEntry_status = cur.fetchall()
             
                if updateEntry_status == ():
                    update_status='0'
                else:
                    update_status='2'  
         
                str3 =(f"""INSERT INTO daily_mainentry(userid, date, totalTime, createDate, createTime,status)VALUES( %s, %s, %s,%s, %s,%s)""")
                values = (Empid, entryDate, totalDuration,entryDate,timeIn,update_status)
                cur.execute(str3,values)
                conn.commit()
        
    return jsonify({'status': 200, 'message': 'Daily Entry  Successfull!'})  

@app.route('/CurrentStatus_show/<empid>/<date>', methods=['GET'])
def CurrentStatus_show(empid,date):

    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)   
    str2 = "SELECT status FROM daily_attendanceentry where userid='"+empid+"' and date='"+date+"' order by id desc limit 1 " 
    cur.execute(str2)
    check_currentStatus = cur.fetchall()

    sendStatus=check_currentStatus[0]['status']
    return jsonify({'data':sendStatus})
def serialize_timedelta(obj):
    if isinstance(obj, timedelta):
        return str(obj)  
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
@app.route('/viewDailyentry/<empid>/<date>',methods=['GET'])
def dailyEntryview(empid,date):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor) 
    str2 = "SELECT userid,status,date,timeIn FROM emp_register.daily_attendanceentry where userid='"+empid+"' and date='"+date+"' " 
    cur.execute(str2)
    data = cur.fetchall()

    for entry in data:
        entry['timeIn'] = str(entry['timeIn'])
        entry['date']=str(entry['date'])

    combined_data = []
    temp_entry = None
    total_time = timedelta()

    for entry in data:
        if entry['status'] == '1':
            if temp_entry:
                temp_entry['timeOut'] = entry['timeIn']
                time_in = datetime.strptime(temp_entry['timeIn'], "%H:%M:%S")
                time_out = datetime.strptime(temp_entry['timeOut'], "%H:%M:%S")
                total_time += time_out - time_in
                temp_entry['TotalTime'] = str(total_time)
                combined_data.append(temp_entry)
            temp_entry = {
                'userid': entry['userid'],
                'date': entry['date'],
                'timeIn': entry['timeIn'],
                'timeOut': entry['timeIn']
                    }
        elif entry['status'] == '0' and temp_entry:
            temp_entry['timeOut'] = entry['timeIn']
            time_in = datetime.strptime(temp_entry['timeIn'], "%H:%M:%S")
            time_out = datetime.strptime(temp_entry['timeOut'], "%H:%M:%S")
            total_time += time_out - time_in
            temp_entry['TotalTime'] = str(total_time)
            combined_data.append(temp_entry)
            temp_entry = None

    if temp_entry:
        # temp_entry['timeOut'] = '00:00:00'
        temp_entry['timeOut'] = ''
        # temp_entry['TotalTime'] = str(total_time)
        combined_data.append(temp_entry) 


    return jsonify({'data':combined_data})

@app.route('/ticketChat/<empid>',methods=['GET'])  
def ticketChat(empid):
     conn = mysql.connect()
     cur = conn.cursor(pymysql.cursors.DictCursor)
     str=f"""SELECT * FROM employee_data where id='{empid}' and Approved=0;"""
     cur.execute(str)
     loginData = cur.fetchall()
     conn.commit()
     
     return jsonify({'data':loginData})

@app.route('/chatTicket_list/<empid>/<limit>',methods=['GET'])
def chatTicket_list(empid,limit):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    str1 = (f"""SELECT a.id, MAX(a.user_id) AS user_id, MAX(a.To_Email) AS To_Email,MAX(a.Subject) AS Subject,MAX(a.Message) AS Message,MAX(a.status) AS status,MAX(b.id) AS id,MAX(b.ticketid) AS ticketid,MAX(b.userid) AS userid,MAX(b.CC_Emails) AS CC_Emails,MAX(c.firstname) AS firstname,MAX(c.lastname) AS lastname
    FROM emp_register.ticketrise_table AS a
    LEFT JOIN emp_register.ccemail_data AS b ON b.userid = a.user_id
    LEFT JOIN emp_register.employee_data AS c ON c.id = a.user_id
    WHERE a.To_Email = '{empid}' OR b.CC_Emails = '{empid}'
    GROUP BY a.id  LIMIT %s """ %(limit))  
    cur.execute(str1)
    listingData = cur.fetchall()
    conn.commit()
     
    return jsonify({'data':listingData})
@app.route('/Chating_employeelist',methods=['GET'])
def Chating_employeelist():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    str1 = (f"""SELECT * FROM employee_data where  Approved=0; """)  
    cur.execute(str1)
    listingEmp = cur.fetchall()
    conn.commit()
     
    return jsonify({'data':listingEmp})

@app.route('/chatActive_update',methods=['PUT'])
def chatActiveStatus():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
     
    # str1 = "update emp_register.daily_mainentry set chatActive='Active'  WHERE id='10' ";
    # cur.execute(str1)
    # conn.commit()
    return jsonify({'status': 200, 'message': 'Daily Entry  Successfull!'})  
@app.route('/chatActive_update/<id>/<activeStatus>', methods=['PUT'])
def Actstatus_update(id,activeStatus):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    str = f"""update employee_data set  chatActive='{activeStatus}' WHERE id='{id}';"""
    cur.execute(str)
    conn.commit()
    return jsonify({'status': 200, 'msg': 'status update!'})

@app.route('/update_status/<user_id>/<activeStatus>', methods=['GET'])
def update_status(user_id,activeStatus):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    str = f"""update employee_data set  chatActive='{activeStatus}' WHERE id='{user_id}';"""
    cur.execute(str)
    conn.commit()

    return "Status updated successfully", 200





 
    



    
if __name__ == '__main__':
    app.run(debug=True)

