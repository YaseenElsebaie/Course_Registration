#Created by Yaseen Elsebaie
#December 10th, 2023

from asyncio.format_helpers import _get_function_source
from calendar import c, month
from cgitb import Hook
from distutils.log import error
from fnmatch import fnmatchcase
from functools import total_ordering
from math import remainder
from re import A
import re
from select import select
from sre_parse import GLOBAL_FLAGS
from sys import get_coroutine_origin_tracking_depth
from sysconfig import get_paths
from this import d
from webbrowser import get
from zoneinfo import available_timezones
import re
import yaml
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from queries import *
from db import *


#Initialize the app from Flask
app = Flask(__name__, static_folder='Images')


#Configure MySQL and server
conn = pymysql.connect(host='localhost', 
					   port= 3306,
                       user='root',
                       password='',
                       db='Tandon',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)



# Define a route to the homepage
@app.route('/', methods=['GET', 'POST'])
def homepage():
	
	return render_template('Homepage.html')


# Define a route to the logins page for students, instructors, and admins
@app.route('/Login')
def login():

	return render_template('Logins.html')



# Define route for student login authentication
@app.route('/StudentloginAuth', methods=['GET', 'POST'])
def StudentloginAuth():
	
	#grabs student login information from the forms
	Student_ID = request.form['Student_ID']
	password = request.form['Student_Password']
    

	cursor = conn.cursor()
	
	#executes query to check if student login is correct
	query = 'SELECT Student_ID, Student_Password FROM Student WHERE Student_ID = %s and Student_Password = %s'
	cursor.execute(query, (Student_ID, password))
	data = cursor.fetchone()


	error = None

	#checks if student exists and then directs to student home
	if(data):
		# assign all sessions 
		session['Student_ID'] = Student_ID

		# Fetches student information for displaying on hommepage
		Student_ID=session['Student_ID']
		query2 = "Select * from Student where Student_ID=%s"
		cursor.execute(query2, (Student_ID))
		student = cursor.fetchone()
		cursor.close()
	
		return render_template('StudentHome.html', error=error, Student_ID=session['Student_ID'],student=student)
	
	else:	#if student does not exist
		#returns an error message to the html page
		error = 'Invalid login or username'
		cursor.close()
		return render_template('Logins.html', error=error)



# Define route for instructor login authentication
@app.route('/InstructorloginAuth', methods=['GET', 'POST'])
def InstructorloginAuth():
	
	#grabs instructor login information from the forms
	Instructor_ID = request.form['Instructor_ID']
	password = request.form['Instructor_Password']
    
	# Hashes the password
	# password=hashlib.md5(password.encode())

	cursor = conn.cursor()
	
	#executes query to check if instrcutor login is correct
	query = 'SELECT Instructor_ID, Instructor_Password FROM Instructor WHERE Instructor_ID = %s and Instructor_Password = %s'
	cursor.execute(query, (Instructor_ID, password))
	data = cursor.fetchone()
	
	error = None

	#checks if the instructor exists
	if(data):
		# assign sessions 
		session['Instructor_ID']=Instructor_ID

		#Gets instructor information to display on instructor homepage
		query2 = "Select * from Instructor where Instructor_ID=%s"
		cursor.execute(query2, (Instructor_ID))
		instructor = cursor.fetchone()
		cursor.close()
		return render_template('InstructorHome.html', error=error, instructor=instructor)

	else:
		#returns an error message to the html page if login is not valid
		error = 'Invalid login or username'
		return render_template('Logins.html', error=error)



# Define route for admin login authentication
@app.route('/AdminloginAuth', methods=['GET', 'POST'])
def AdminloginAuth():
	
	#grabs admin login information from the forms
	Admin_ID = request.form['Admin_ID']
	password = request.form['Admin_Password']
    
	# Hashes the password
	# password=hashlib.md5(password.encode())

	cursor = conn.cursor()

	#executes query to check if admin ogin is correct
	query = 'SELECT Admin_ID, Admin_Password FROM Administrator WHERE Admin_ID = %s and Admin_Password = %s'
	cursor.execute(query, (Admin_ID, password))
	data = cursor.fetchone()

	cursor.close()

	error = None

	#checks if admin exists and routes to admin homepage
	if(data):
		# assign all sessions 
		session['Admin_ID']=Admin_ID
		return render_template('AdminHome.html', error=error, Admin_ID=session['Admin_ID'])

	else:		#if admin doesnt exist
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('Logins.html', error=error)



# route to student registration page
@app.route('/Register')
def register():
     
	return render_template('Register.html')


# route to Calendar page
@app.route('/Calendar')
def Calendar():

	return render_template('Calendar.html')


# route to Calendar page from student home
@app.route('/StudentCalendar')
def StudentCalendar():

	return render_template('StudentCalendar.html')


# route to admin homepage
@app.route('/AdminHome')
def AdminHome():

	return render_template('AdminHome.html', Admin_ID=session['Admin_ID'])



# route to instructor homepage
@app.route('/InstructorHome')
def InstructorHome():
		
	cursor = conn.cursor()

	#Query that Gets instructor information to display it on instructor homepage after login
	query2 = "Select * from Instructor where Instructor_ID=%s"
	cursor.execute(query2, (session['Instructor_ID']))
	instructor = cursor.fetchone()
	cursor.close()

	return render_template('InstructorHome.html', error=error, instructor=instructor)



# route to student homepage
@app.route('/StudentHome')
def StudentHome(): 

	#Query to fetch student information for displaying on student homepage after login
	cursor = conn.cursor()
	Student_ID=session['Student_ID']
	query2 = "Select * from Student where Student_ID=%s"
	cursor.execute(query2, (Student_ID))
	student = cursor.fetchone()
	cursor.close()

	return render_template('StudentHome.html', student=student)



#logout for student 
@app.route('/StudentLogout')
def StudentLogout():

	# Clear all the session variables related to the student and logout
	session.pop('Student_ID')
 
	return redirect('/')


#logout for Instructor
@app.route('/InstructorLogout')
def InstructorLogout():

	# Clear all the session variables related to the instructor and logout
	session.pop('Instructor_ID')
	
	return redirect('/')



#logout for Admin
@app.route('/AdminLogout')
def AdminLogout():

	# Clear all the session variables related to the admin and logout
	session.pop('Admin_ID')
	
	return redirect('/')



# route to insert the student info into the database
@app.route('/StudentRegister',  methods=['GET', 'POST'])
def student_register():

   # get the student profile values from the form inputs 
	Student_ID = request.form['Student_ID']
	Student_Password = request.form['Student_Password']
	Student_Fname = request.form['Student_Fname']
	Student_Lname = request.form['Student_Lname']
	Major = request.form['Major']
	Credits_Taken = request.form['Credits_Taken']

	cursor =conn.cursor()
	
	try:

		#Query to Register a student and create profile with form values
		query1= "INSERT INTO Student (Student_ID, Student_Password, Student_Fname, Student_Lname, Major, Credits_Taken) VALUES (%s, %s,%s, %s, %s, %s)"
		cursor.execute(query1, (Student_ID, Student_Password, Student_Fname, Student_Lname, Major, Credits_Taken))
		conn.commit()
		
		cursor.close()
		
		return redirect('/')

	except Exception as e:		#if error when inserting student to database
		
		conn.rollback()
		error = str(e)
		return render_template('Register.html', error=error)
    
	finally:
		cursor.close()
		return redirect('/')



#route to search for courses based on course name
@app.route('/CourseSearchName',  methods=['GET', 'POST'])
def Course_Search_Name():

	#get course name for search from the input
	Course_Name = request.form['Course_Name']

	#Query to get all available courses with that name
	cursor =conn.cursor()
	get_courses = 'SELECT * FROM Course WHERE Course_Name=%s'
	cursor.execute(get_courses, (Course_Name))
	Courses=cursor.fetchall()

	#Query to get all available Sections for the courses
	get_sections = 'Select * FROM Section WHERE Course_Name=%s'
	cursor.execute(get_sections,(Course_Name))
	Sections=cursor.fetchall()

	cursor.close()

	return render_template('SearchByName.html', Courses =Courses, Sections=Sections)



#route to search for courses based on instructor name
@app.route('/CourseSearchInstructor',  methods=['GET', 'POST'])
def Course_Search_Instructor():

	#get instructor name for the search from the user input
	Instructor_Name = request.form['Instructor_Name']

	#Query to get all available courses 
	cursor =conn.cursor()
	get_courses = 'SELECT * FROM Course Natural Join Section Natural Join Teaches Natural Join Instructor WHERE Instructor_Fname=%s'
	cursor.execute(get_courses, (Instructor_Name))
	Courses=cursor.fetchall()

	#Query to get all available Sections for the courses
	get_sections = 'Select * FROM Teaches Natural Join Section Natural Join Instructor WHERE Instructor_Fname=%s'
	cursor.execute(get_sections,(Instructor_Name))
	Sections=cursor.fetchall()

	cursor.close()

	return render_template('SearchByInstructor.html', Courses =Courses, Sections=Sections, Instructor_Name=Instructor_Name)



#route to Search for courses by department
@app.route('/CourseSearchDepartment',  methods=['GET', 'POST'])
def Course_Search_Dept():

	#get department name for search from the input
	Department_Name = request.form['Department_Name']

	#Query to get all available courses 
	cursor =conn.cursor()
	get_courses = 'SELECT * FROM Course WHERE Department_Name=%s'
	cursor.execute(get_courses, (Department_Name))
	Courses=cursor.fetchall()

	#Query to get all available Sections for the courses
	get_sections = 'Select * FROM Section Natural Join Course WHERE Department_Name=%s'
	cursor.execute(get_sections,(Department_Name))
	Sections=cursor.fetchall()

	cursor.close()

	return render_template('SearchByDepartment.html', Courses =Courses, Sections=Sections, Department_Name=Department_Name)



# Route to student's taken courses page
@app.route('/StudentCourses')
def StudentCourses():
	
	Student = session['Student_ID']
	
	#Query to fetch all course details taken by student
	cursor =conn.cursor()
	get_courses = 'SELECT * FROM Takes Natural Join Course WHERE Student_ID=%s'
	cursor.execute(get_courses, (Student))
	takes=cursor.fetchall()
	cursor.close()

	return render_template('StudentCourses.html', takes = takes)



#function and route for rating courses
@app.route("/CourseRating",methods=['GET', 'POST'])
def Rating():

	if ('Confirm' in request.form):		#Check is student chooses to update the rating

		cursor =conn.cursor()
		
		#Get Values from the form
		Rating = request.form['Rating']
		Confirm = request.form['Confirm']

		Student = session['Student_ID']

		Confirm=yaml.safe_load(Confirm)

		Section_ID =  Confirm['Section_ID']
		Course_ID = Confirm['Course_ID']

		#Executes query for inserting rating
		insert_rating="UPDATE Takes SET Rating = %s WHERE (Student_ID = %s) and (Section_ID = %s) and (Course_ID = %s)"
		cursor.execute(insert_rating,(Rating, Student, Section_ID, Course_ID))
		conn.commit()
			
		cursor.close()
		
	return redirect('/StudentHome')


# Route to page for student to begin search for available courses
@app.route('/CourseRegistration', methods=['GET','POST'])
def CourseRegistration():
	
	return render_template('CourseRegistrationSearch.html')



#Route for page for admin to create course
@app.route('/AdminCreateCourse')
def AdminCreateCourse():
	
	return render_template('AdminCreateCourse.html')



#create and insert course into database function
@app.route('/AdminInsertCourse', methods=['GET', 'POST'])
def AdminInsertCourse():

	#Get Course and section info for the new course and section being created
	Course_ID = request.form['Course_ID']
	Course_Name= request.form['Course_Name']
	Course_Credits= request.form['Course_Credits']
	Course_Description= request.form['Course_Description']
	
	Department_Name= request.form['Department_Name']
	Section_ID = request.form['Section_ID']
	Semester = request.form['Semester']
	Section_Day = request.form['Section_Day']
	Section_Time = request.form['Section_Time']
	Student_Limit = request.form['Student_Limit']

	try:

		#execute query to add the course
		cursor = conn.cursor()
		query = "INSERT INTO Course (Course_ID, Course_Name, Course_Credits, Course_Description, Department_Name ) VALUES (%s, %s,%s, %s, %s)"
		cursor.execute(query,(Course_ID, Course_Name, Course_Credits, Course_Description, Department_Name))
		conn.commit()

		#execute query to add the section
		cursor = conn.cursor()
		query2 = "INSERT INTO Section (Section_ID, Course_ID, Course_Name, Semester, Section_Day, Section_Time, Student_Limit ) VALUES (%s, %s,%s, %s, %s, %s, %s)"
		cursor.execute(query2,(Section_ID, Course_ID, Course_Name, Semester, Section_Day, Section_Time, Student_Limit))
		conn.commit()
		cursor.close()

		return redirect(url_for('AdminCreateCourse'))
	
	except Exception as e:		#if inserting course or section fails

		conn.rollback()
		error = str(e)
		return render_template('AdminCreateCourse.html', error=error)



#Route for admin page to create section
@app.route('/AdminCreateSection')
def AdminCreateSection():
	
	return render_template('AdminCreateSection.html')



#create and insert section into database function
@app.route('/AdminInsertSection', methods=['GET', 'POST'])
def AdminInsertSection():

	#Get Section info for the new section being created
	Course_ID = request.form['Course_ID']
	Course_Name= request.form['Course_Name']
	Section_ID = request.form['Section_ID']
	Semester = request.form['Semester']
	Section_Day = request.form['Section_Day']
	Section_Time = request.form['Section_Time']
	Student_Limit = request.form['Student_Limit']

	#execute query to check the course
	cursor = conn.cursor()
	query = "Select * FROM Course Where Course_ID = %s"
	cursor.execute(query,(Course_ID))
	course = cursor.fetchall()


	if (course):

		#execute query to add the section
		cursor = conn.cursor()
		query2 = "INSERT INTO Section (Section_ID, Course_ID, Course_Name, Semester, Section_Day, Section_Time, Student_Limit ) VALUES (%s, %s,%s, %s, %s, %s, %s)"
		cursor.execute(query2,(Section_ID, Course_ID, Course_Name, Semester, Section_Day, Section_Time, Student_Limit))
		conn.commit()
	else:
		#returns an error message to the html page
		error = 'Invalid Course ID'
		return render_template('AdminCreateSection.html', error=error)

	cursor.close()

	return redirect(url_for('AdminCreateSection'))



#Route for page with form to assign an instructor to a section
@app.route('/AssignInstructor')
def AssignInstructor():
	
	return render_template('AssignInstructor.html')



#assign professor to a section and update database function
@app.route('/InsertTeaches', methods=['GET', 'POST'])
def InsertTeaches():

	#Get form values to assign instructor
	Course_ID = request.form['Course_ID']
	Section_ID = request.form['Section_ID']
	Instructor_ID = request.form['Instructor_ID']

	#execute query to fetch all details of the course
	cursor = conn.cursor()
	query = "Select * FROM Course Where Course_ID = %s"
	cursor.execute(query,(Course_ID))
	course = cursor.fetchall()

	#execute query to fetch all details of the section
	cursor = conn.cursor()
	query = "Select * FROM Section Where Section_ID = %s and Course_ID = %s"
	cursor.execute(query,(Section_ID, Course_ID))
	section = cursor.fetchall()
	

	if (course and section): #Check if course and section exist

		#execute query to assign the instructor to teach
		cursor = conn.cursor()
		query2 = "INSERT INTO Teaches (Section_ID, Course_ID, Instructor_ID) VALUES (%s, %s,%s)"
		cursor.execute(query2,(Section_ID, Course_ID, Instructor_ID))
		conn.commit()

	else: #if course or section dont exist
		error = 'Invalid Section'
		return render_template('AssignInstructor.html', error=error)

	cursor.close()
	return redirect(url_for('AssignInstructor'))



#Route for instrcutor page to create course
@app.route('/InstructorCreateCourse')
def InstructorCreateCourse():

	return render_template('InstructorCreateCourse.html')



#create and insert course into database function
@app.route('/InstructorInsertCourse', methods=['GET', 'POST'])
def InstructorInsertCourse():

	#Get Course and section info for the new course and section being created
	Course_ID = request.form['Course_ID']
	Course_Name= request.form['Course_Name']
	Course_Credits= request.form['Course_Credits']
	Course_Description= request.form['Course_Description']
	
	Department_Name= request.form['Department_Name']
	Section_ID = request.form['Section_ID']
	Semester = request.form['Semester']
	Section_Day = request.form['Section_Day']
	Section_Time = request.form['Section_Time']
	Student_Limit = request.form['Student_Limit']

	try:

		#execute query to add the course
		cursor = conn.cursor()
		query = "INSERT INTO Course (Course_ID, Course_Name, Course_Credits, Course_Description, Department_Name ) VALUES (%s, %s,%s, %s, %s)"
		cursor.execute(query,(Course_ID, Course_Name, Course_Credits, Course_Description, Department_Name))
		conn.commit()

		#execute query to add the section
		cursor = conn.cursor()
		query2 = "INSERT INTO Section (Section_ID, Course_ID, Course_Name, Semester, Section_Day, Section_Time, Student_Limit ) VALUES (%s, %s,%s, %s, %s, %s, %s)"
		cursor.execute(query2,(Section_ID, Course_ID, Course_Name, Semester, Section_Day, Section_Time, Student_Limit))
		conn.commit()
		cursor.close()

		return redirect(url_for('InstructorCreateCourse'))
	
	except Exception as e:		#if inserting course or section fails

		conn.rollback()
		error = str(e)
		return render_template('InstructorCreateCourse.html', error=error)



#Route for instructor page to create section
@app.route('/InstructorCreateSection')
def InstructorCreateSection():

	return render_template('InstructorCreateSection.html')



#create and insert section into database
@app.route('/InstructorInsertSection', methods=['GET', 'POST'])
def InstructorInsertSection():

	#Get Section info for the new section being created
	Course_ID = request.form['Course_ID']
	Course_Name= request.form['Course_Name']
	Section_ID = request.form['Section_ID']
	Semester = request.form['Semester']
	Section_Day = request.form['Section_Day']
	Section_Time = request.form['Section_Time']
	Student_Limit = request.form['Student_Limit']

	#execute query to check if course exists
	cursor = conn.cursor()
	query = "Select * FROM Course Where Course_ID = %s"
	cursor.execute(query,(Course_ID))
	course = cursor.fetchall()


	if (course):	#if the course exists then create section

		#execute query to add the section
		cursor = conn.cursor()
		query2 = "INSERT INTO Section (Section_ID, Course_ID, Course_Name, Semester, Section_Day, Section_Time, Student_Limit ) VALUES (%s, %s,%s, %s, %s, %s, %s)"
		cursor.execute(query2,(Section_ID, Course_ID, Course_Name, Semester, Section_Day, Section_Time, Student_Limit))
		conn.commit()

	else:		# if course doesnt exist, return error message

		error = 'Invalid Course ID'
		return render_template('InstructorCreateSection.html', error=error)

	cursor.close()

	return redirect(url_for('InstructorCreateSection'))

#Route for admin page to create instructor account
@app.route('/CreateInstructor')
def CreateInstructor():
	
	return render_template('CreateInstructor.html')



#create and insert instructor into database 
@app.route('/InsertInstructor', methods=['GET', 'POST'])
def InsertInstructor():

	#Get values from the form for instructor new account
	Instructor_ID = request.form['Instructor_ID']
	Instructor_Password = request.form['Instructor_Password']
	Instructor_Fname = request.form['Instructor_Fname']
	Instructor_Lname = request.form['Instructor_Lname']
	Instructor_Email = request.form['Instructor_Email']
	Department_Name = request.form['Department_Name']
	

	try:

		#execute query to add the instructor account
		cursor = conn.cursor()
		query = "INSERT INTO Instructor (Instructor_ID, Instructor_Password, Instructor_Fname, Instructor_Lname, Instructor_Email, Department_Name) VALUES (%s, %s, %s, %s, %s, %s)"
		cursor.execute(query,(Instructor_ID, Instructor_Password, Instructor_Fname, Instructor_Lname, Instructor_Email, Department_Name))
		conn.commit()
		cursor.close()

		return redirect(url_for('CreateInstructor'))
	
	except Exception as e:	#if inserting instructor to database fails return error

		conn.rollback()
		error = str(e)
		return render_template('CreateInstructor.html', error=error)



#Route for admin page to create new department
@app.route('/CreateDepartment')
def CreateDepartment():
	
	return render_template('CreateDepartment.html')



#create and insert department into database
@app.route('/InsertDepartment', methods=['GET', 'POST'])
def InsertDepartment():

	#Get department details from form inputs
	Department_Name = request.form['Department_Name']
	Department_Address = request.form['Department_Address']
	Department_Email = request.form['Department_Email']
	
	try:

		#execute query to add the department
		cursor = conn.cursor()
		query = "INSERT INTO Department (Department_Name, Department_Address, Department_Email) VALUES (%s, %s, %s)"
		cursor.execute(query,(Department_Name, Department_Address, Department_Email))
		conn.commit()
		cursor.close()

		return redirect(url_for('CreateDepartment'))
	
	except Exception as e:		#if creating department fails return error

		conn.rollback()
		error = str(e)
		return render_template('CreateDepartment.html', error=error)



#Route for admin page to create new admin account
@app.route('/CreateAdmin')
def CreateAdmin():
	
	return render_template('CreateAdmin.html')



#create and insert new Admin account into database
@app.route('/InsertAdmin', methods=['GET', 'POST'])
def InsertAdmin():

	#Get new admin account details from form inputs
	Admin_ID = request.form['Admin_ID']
	Admin_Password= request.form['Admin_Password']

	try:

		#execute query to add the admin account
		cursor = conn.cursor()
		query = "INSERT INTO Administrator (Admin_ID, Admin_Password) VALUES (%s, %s)"
		cursor.execute(query,(Admin_ID, Admin_Password))
		conn.commit()
		cursor.close()

		return redirect(url_for('CreateAdmin'))
	
	except Exception as e:		#if creating admin account fails return error

		conn.rollback()
		error = str(e)
		return render_template('CreateAdmin.html', error=error)



#page route and function for viewing the instructor's courses 
@app.route('/ViewInstructorCourses')
def ViewInstructorCourses():
	
	Instructor = session['Instructor_ID']
	
	#Executes query to fetch details of all courses taught by this instructor
	cursor =conn.cursor()
	get_courses = 'SELECT * FROM Teaches WHERE Instructor_ID=%s'
	cursor.execute(get_courses, (Instructor))
	teaches=cursor.fetchall()

	cursor.close()

	return render_template('InstructorCourses.html', teaches=teaches)



#page route and function for viewing the students in the instructor's chosen course
@app.route('/CourseStudents',methods=['GET', 'POST'])
def CourseStudents():
	
	if 'View_Students' in request.form:	#checks if instructor would like to view their courses
		
		cursor =conn.cursor()
		Course = request.form['View_Students']
		Course=yaml.safe_load(Course)
		
		Instructor = session["Instructor_ID"]
		Course_ID= Course['Course_ID']
		Section_ID = Course['Section_ID']
		
		#Executes query for getting students based on course and section ID and instructor teaching
		get_students="Select * from (Takes Natural Join Student Natural Join Teaches)  where (Course_ID = %s) and (Section_ID = %s) and (Instructor_ID = %s)"
		cursor.execute(get_students,(Course_ID, Section_ID, Instructor))
		students =  cursor.fetchall()
		conn.commit()
		
		cursor.close()
		
		return render_template('StudentsInCourse.html', students=students, Course_ID=Course_ID)

	return redirect(url_for('ViewInstructorCourses'))



#page route and function for updating a students grade in the database
@app.route('/GradeStudents',methods=['GET', 'POST'])
def GradeStudents():
	
	
	if ('Confirm' in request.form):		#Check if instructor would like to update and fetches which student to assign grade to
		
		cursor =conn.cursor()
		
		#Get grade value from instructor input to update database
		Grade = request.form['Grade']
		Confirm = request.form['Confirm']
		
		Confirm=yaml.safe_load(Confirm)

		Student = Confirm['Student_ID']
		Section_ID =  Confirm['Section_ID']
		Course_ID = Confirm['Course_ID']

		#Executes query for inserting student grade
		update_grade="UPDATE Takes SET Grade = %s WHERE (Student_ID = %s) and (Section_ID = %s) and (Course_ID = %s)"
		cursor.execute(update_grade,(Grade, Student, Section_ID, Course_ID))
		conn.commit()
			
		cursor.close()
		
	return redirect(url_for('CourseStudents'))



#Page route and function to fetch available sections for student registration based on course name
@app.route('/StudentSearchCourseName', methods=['GET', 'POST'])
def StudentSearchName():
	
	Course_Name = request.form['Course_Name']

	#Query to get available section information
	cursor =conn.cursor()
	get_available_courses = 'SELECT * FROM Section Natural Join Instructor Natural Join Teaches Natural Join Course Natural Join coursesectioncapacitydiff where (Course_Name = %s) and (remaining_spots > 0)'
	cursor.execute(get_available_courses, (Course_Name))
	courses=cursor.fetchall()

	cursor.close()
	
	return render_template('StudentSearchCourseName.html',courses=courses)



#Page route and function to fetch courses for student registration based on department
@app.route('/StudentSearchDepartment', methods=['GET', 'POST'])
def StudentSearchDepartment():
	
	Department_Name = request.form['Department_Name']
	
	#Query to get available section information
	cursor =conn.cursor()
	get_available_courses = 'SELECT * FROM Section Natural Join Course Natural Join Instructor Natural Join Teaches Natural Join coursesectioncapacitydiff where (Department_Name = %s) and (remaining_spots > 0)'
	cursor.execute(get_available_courses, (Department_Name))
	courses=cursor.fetchall()
	cursor.close()


	return render_template('StudentSearchDepartment.html',courses=courses)



#Page route and function to fetch courses for student registration based on instructor
@app.route('/StudentSearchInstructor', methods=['GET', 'POST'])
def StudentSearchInstructor():
	
	Instructor_Name = request.form['Instructor_Name']
	
	#Query to get available section information
	cursor =conn.cursor()
	get_available_courses = 'SELECT * FROM Section Natural Join Teaches Natural Join Instructor Natural Join coursesectioncapacitydiff where (Instructor_Fname = %s) and (remaining_spots > 0)'
	cursor.execute(get_available_courses, (Instructor_Name))
	courses=cursor.fetchall()

	cursor.close()
	
	return render_template('StudentSearchInstructor.html',courses=courses)



#page route and function for adding a student to a section
@app.route('/Register', methods=['GET', 'POST'])
def Register():

	if ('Register' in request.form):		#Checks if student chose to register
		cursor =conn.cursor()
		
		#Fetches data of which section is chosen
		Register = request.form['Register']
		
		Register=yaml.safe_load(Register)

		Student_ID = session['Student_ID']
		Section_ID =  Register['Section_ID']
		Course_ID = Register['Course_ID']
		
		try:

			#Executes query for inserting student into the section
			Register_query="INSERT INTO Takes (Course_ID, Student_ID, Section_ID) VALUES (%s, %s,%s)"
			cursor.execute(Register_query,(Course_ID, Student_ID, Section_ID))
			conn.commit()

			#executes query to update student credits based on the registered course
			get_credits="Select Course_Credits from Course Where Course_ID = %s"
			cursor.execute(get_credits, Course_ID)
			course_credits = cursor.fetchone()
			Update_Credits="Update Student SET Credits_Taken = Credits_Taken + %s"
			cursor.execute(Update_Credits, course_credits['Course_Credits'])
			conn.commit()

		except Exception as e:		#if registering the student to the section fails return error

			conn.rollback()
			error = str(e)
			return render_template('CourseRegistrationSearch.html', error=error)
			
		cursor.close()
		
	return redirect('/StudentHome')



#page route for admin proposing the section choices to an instructor
@app.route('/ProposeChoice')
def ProposeChoice():

	return render_template('AdminProposeChoice.html')



#page route and function for admin proposing the section choices to an instructor in the database
@app.route('/InsertChoice', methods=['GET', 'POST'])
def InsertChoice():

	Admin_ID = session['Admin_ID']

	#fetch all form values to create the section choices for instructor
	Instructor_ID = request.form['Instructor_ID']
	Course_ID = request.form['Course_ID']
	Course_Name= request.form['Course_Name']
	Course_Credits= request.form['Course_Credits']
	Course_Description=request.form['Course_Description']
	Department_Name= request.form['Department_Name']
	Semester = request.form['Semester']
	Student_Limit = request.form['Student_Limit']

	#Fetch section option 1 info from form
	Section_ID = request.form['Section_ID']
	Section_Day = request.form['Section_Day']
	Section_Time = request.form['Section_Time']	

	#Fetch section option 2 info from form
	Section2_ID = request.form['Section2_ID']
	Section2_Day = request.form['Section2_Day']
	Section2_Time = request.form['Section2_Time']


	try:

		#execute query to add the choice to the database for instrcutor to choose
		cursor = conn.cursor()
		query = "INSERT INTO Choice (Admin_ID, Instructor_ID, Course_ID, Course_Name, Course_Credits, Course_Description, Department_Name, Semester, Student_Limit, Section_ID, Section_Day, Section_Time, Section2_ID, Section2_Day, Section2_Time) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s)"
		cursor.execute(query,(Admin_ID, Instructor_ID, Course_ID, Course_Name, Course_Credits, Course_Description, Department_Name, Semester, Student_Limit, Section_ID, Section_Day, Section_Time, Section2_ID, Section2_Day, Section2_Time))
		conn.commit()

		cursor.close()
		return render_template('AdminProposeChoice.html')

	except Exception as e:		#if adding the choice fails returns error

		conn.rollback()
		error = str(e)

		return render_template('AdminProposeChoice.html', error=error)



#page route for instructor viewing proposed sections
@app.route('/ViewChoice')
def ViewChoice():

	Instructor_ID = session['Instructor_ID']

	#Fetches the most recent choice options for the instructor to choose
	cursor =conn.cursor()
	get_choice = 'SELECT * FROM Choice where Instructor_ID = %s'
	cursor.execute(get_choice, (Instructor_ID))
	line=cursor.fetchone()

	return render_template('InstructorChoice.html', line= line)



#create and insert course and section based on instructor choice into database function
@app.route('/InsertSectionChoice', methods=['GET', 'POST'])
def InsertSectionChoice():

	Instructor_ID = session['Instructor_ID']

	cursor =conn.cursor()
	get_choice = 'SELECT * FROM Choice where Instructor_ID = %s'
	cursor.execute(get_choice, (Instructor_ID))
	course=cursor.fetchone()
	
	Selected_Section = request.form['Selected_Section']

	if (Selected_Section == 'Section1'):	#if chosen section is the first section
		
		#Query to create the new course
		query = "INSERT INTO Course (Course_ID, Course_Name, Course_Credits, Course_Description, Department_Name ) VALUES (%s, %s,%s, %s, %s)"
		cursor.execute(query,(course['Course_ID'], course['Course_Name'], course['Course_Credits'], course['Course_Description'], course['Department_Name']))
		conn.commit()

		#Query to create the new section
		section1_query = "INSERT INTO Section (Section_ID, Course_ID, Course_Name, Semester, Section_Day, Section_Time, Student_Limit ) VALUES (%s, %s,%s, %s, %s, %s, %s)"
		cursor.execute(section1_query,(course['Section_ID'], course['Course_ID'], course['Course_Name'], course['Semester'], course['Section_Day'], course['Section_Time'], course['Student_Limit']))
		conn.commit()

		#Query to assign the instructor to the new section
		teaches1 = "Insert Into Teaches (Course_ID, Instructor_ID, Section_ID) VALUES (%s, %s, %s)"
		cursor.execute(teaches1,(course['Course_ID'], Instructor_ID, course['Section_ID']))
		conn.commit()

		#Query to delete the choice options after the section is chosen and created
		delete_choice = "DELETE FROM Choice WHERE Instructor_ID = %s AND Course_ID = %s AND Section_ID = %s AND Section2_ID = %s"
		cursor.execute(delete_choice, (Instructor_ID, course['Course_ID'], course['Section_ID'], course['Section2_ID']))
		conn.commit()



	elif (Selected_Section == 'Section2'):		#if chosen section is the second section

		#Query to create the new course
		query = "INSERT INTO Course (Course_ID, Course_Name, Course_Credits, Course_Description, Department_Name ) VALUES (%s, %s,%s, %s, %s)"
		cursor.execute(query,(course['Course_ID'], course['Course_Name'], course['Course_Credits'], course['Course_Description'], course['Department_Name']))
		conn.commit()

		#Query to create the new section
		section2_query = "INSERT INTO Section (Section_ID, Course_ID, Course_Name, Semester, Section_Day, Section_Time, Student_Limit ) VALUES (%s, %s,%s, %s, %s, %s, %s)"
		cursor.execute(section2_query,(course['Section2_ID'], course['Course_ID'], course['Course_Name'], course['Semester'], course['Section2_Day'], course['Section2_Time'], course['Student_Limit']))
		conn.commit()

		#Query to assign the instructor to the new section
		teaches2 = "Insert Into Teaches (Course_ID, Instructor_ID, Section_ID) VALUES (%s, %s, %s)"
		cursor.execute(teaches2,(course['Course_ID'], Instructor_ID, course['Section2_ID']))
		conn.commit()

		#Query to delete the choice options after the section is chosen and created
		delete2_choice = "DELETE FROM Choice WHERE Instructor_ID = %s AND Course_ID = %s AND Section_ID = %s AND Section2_ID = %s"
		cursor.execute(delete2_choice, (Instructor_ID, course['Course_ID'], course['Section_ID'], course['Section2_ID']))
		conn.commit()
		

	cursor.close()

	return redirect('/InstructorHome')

# def create_course_and_section(course_data, section_data, instructor_id):
#     cursor = conn.cursor()

#     # Query to create the new course
#     query = "INSERT INTO Course (Course_ID, Course_Name, Course_Credits, Course_Description, Department_Name ) VALUES (%s, %s,%s, %s, %s)"
#     cursor.execute(query, (course_data['Course_ID'], course_data['Course_Name'], course_data['Course_Credits'], course_data['Course_Description'], course_data['Department_Name']))
#     conn.commit()

#     # Query to create the new section
#     section_query = "INSERT INTO Section (Section_ID, Course_ID, Course_Name, Semester, Section_Day, Section_Time, Student_Limit ) VALUES (%s, %s,%s, %s, %s, %s, %s)"
#     cursor.execute(section_query, (section_data['Section_ID'], course_data['Course_ID'], course_data['Course_Name'], course_data['Semester'], section_data['Section_Day'], section_data['Section_Time'], section_data['Student_Limit']))
#     conn.commit()

#     # Query to assign the instructor to the new section
#     teaches_query = "INSERT INTO Teaches (Course_ID, Instructor_ID, Section_ID) VALUES (%s, %s, %s)"
#     cursor.execute(teaches_query, (course_data['Course_ID'], instructor_id, section_data['Section_ID']))
#     conn.commit()

#     cursor.close()

# def delete_choice_option(instructor_id, course_id, section_id, section2_id):
#     cursor = conn.cursor()

#     # Query to delete the choice options after the section is chosen and created
#     delete_choice = "DELETE FROM Choice WHERE Instructor_ID = %s AND Course_ID = %s AND Section_ID = %s AND Section2_ID = %s"
#     cursor.execute(delete_choice, (instructor_id, course_id, section_id, section2_id))
#     conn.commit()

#     cursor.close()

# @app.route('/InsertSectionChoice', methods=['GET', 'POST'])
# def InsertSectionChoice():
#     instructor_id = session['Instructor_ID']
#     selected_section = request.form['Selected_Section']
#     cursor = conn.cursor()

#     get_choice_query = 'SELECT * FROM Choice WHERE Instructor_ID = %s'
#     cursor.execute(get_choice_query, (instructor_id,))
#     choice = cursor.fetchone()

#     if selected_section == 'Section1':
#         create_course_and_section(choice, choice, instructor_id)
#         delete_choice_option(instructor_id, choice['Course_ID'], choice['Section_ID'], choice['Section2_ID'])
#     elif selected_section == 'Section2':
#         create_course_and_section(choice, choice, instructor_id)
#         delete_choice_option(instructor_id, choice['Course_ID'], choice['Section_ID'], choice['Section2_ID'])

#     cursor.close()

#     return redirect('/InstructorHome')



app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
