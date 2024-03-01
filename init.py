#Created by Yaseen Elsebaie

from asyncio.format_helpers import _get_function_source
from calendar import c, month
from cgitb import Hook
from distutils.log import error
from fnmatch import fnmatchcase
from functools import total_ordering
from math import remainder
from re import A
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

	#executes query to check if student login is correct
	data = fetch_one(STUDENT_LOGIN, (request.form['Student_ID'], request.form['Student_Password']))

	error = None

	#checks if student exists and then directs to student home
	if(data):
		# assign all sessions 
		session['Student_ID'] = request.form['Student_ID']

		# Fetches student information for displaying on hommepage
		student = fetch_one(FETCH_STUDENT, (request.form['Student_ID']))
		return render_template('StudentHome.html', error=error, Student_ID=session['Student_ID'],student=student)
	
	else:	#if student does not exist
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('Logins.html', error=error)



# Define route for instructor login authentication
@app.route('/InstructorloginAuth', methods=['GET', 'POST'])
def InstructorloginAuth():

	#executes query to check if instrcutor login is correct
	data = fetch_one(INST_LOGIN, (request.form['Instructor_ID'], request.form['Instructor_Password']))
	error = None

	#checks if the instructor exists
	if(data):
		# assign sessions 
		session['Instructor_ID']=request.form['Instructor_ID']

		#Gets instructor information to display on instructor homepage
		instructor = fetch_one(FETCH_INST, request.form['Instructor_ID'])
		return render_template('InstructorHome.html', error=error, instructor=instructor)

	else:
		#returns an error message to the html page if login is not valid
		error = 'Invalid login or username'
		return render_template('Logins.html', error=error)



# Define route for admin login authentication
@app.route('/AdminloginAuth', methods=['GET', 'POST'])
def AdminloginAuth():
	
    #executes query to check if admin login is correct
	data = fetch_one(ADMIN_LOGIN, (request.form['Admin_ID'], request.form['Admin_Password']))
	error = None

	#checks if admin exists and routes to admin homepage
	if(data):
		# assign all sessions 
		session['Admin_ID']=request.form['Admin_ID']
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
		
	instructor = fetch_one(INST_INFO, (session['Instructor_ID']))

	return render_template('InstructorHome.html', error=error, instructor=instructor)



# route to student homepage
@app.route('/StudentHome')
def StudentHome(): 

	student = fetch_one(STUDENT_INFO, (session['Student_ID']))

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
	
	try:
		# #Query to Register a student and create profile with form values	
		insert(REGISTER_STUDENT, (request.form['Student_ID'], request.form['Student_Password'], request.form['Student_Fname'], request.form['Student_Lname'], request.form['Major'], request.form['Credits_Taken']))
		
		return redirect('/')

	except Exception as e:		#if error when inserting student to database
		
		conn.rollback()
		error = str(e)
		return render_template('Register.html', error=error)
    
	finally:
		return redirect('/')


#route to search for courses based on course name
@app.route('/CourseSearchName',  methods=['GET', 'POST'])
def Course_Search_Name():


	#Query to get all available courses with that name
	courses = fetch_all(FETCH_COURSE_NAME, request.form['Course_Name'])

	#Get all available Sections for the course name
	sections = fetch_all(FETCH_SECTION_NAME, request.form['Course_Name'])

	return render_template('SearchByName.html', Courses =courses, Sections=sections)


#route to search for courses based on instructor name
@app.route('/CourseSearchInstructor',  methods=['GET', 'POST'])
def Course_Search_Instructor():

	#Query to get all available courses 
	courses = fetch_all(FETCH_COURSE_INST, request.form['Instructor_Name'])

	#Query to get all available Sections taught by instructor
	sections = fetch_all(FETCH_SECTION_INST, request.form['Instructor_Name'])

	return render_template('SearchByInstructor.html', Courses =courses, Sections=sections, Instructor_Name=request.form['Instructor_Name'])


#route to Search for courses by department
@app.route('/CourseSearchDepartment',  methods=['GET', 'POST'])
def Course_Search_Dept():

	#Query to get all available courses in department 
	courses = fetch_all(FETCH_COURSE_DEPT, request.form['Department_Name'])

	#Query to get all available Sections under the department
	sections = fetch_all(FETCH_SECTION_DEPT, request.form['Department_Name'])

	return render_template('SearchByDepartment.html', Courses =courses, Sections=sections, Department_Name=request.form['Department_Name'])


# Route to student's taken courses page
@app.route('/StudentCourses')
def StudentCourses():
	
	#Query to fetch all course details taken by student
	takes = fetch_all(FETCH_STUDENT_COURSES, session['Student_ID'])

	return render_template('StudentCourses.html', takes = takes)


#function and route for rating courses
@app.route("/CourseRating",methods=['GET', 'POST'])
def Rating():

	if ('Confirm' in request.form):		#Check is student chooses to update the rating

		#Get Values from the form
		confirm = request.form['Confirm']

		confirm=yaml.safe_load(confirm)

		#Executes query for inserting rating
		insert(UPDATE_RATING, (request.form['Rating'], session['Student_ID'], confirm['Section_ID'], confirm['Course_ID']) )
			
		
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

	try:
		#execute query to add the course
		insert(CREATE_COURSE, (request.form['Course_ID'], request.form['Course_Name'], request.form['Course_Credits'], request.form['Course_Description'], request.form['Department_Name']))

		#execute query to add the section
		insert(CREATE_SECTION,(request.form['Section_ID'], request.form['Course_ID'], request.form['Course_Name'],  request.form['Semester'], request.form['Section_Day'], request.form['Section_Time'], request.form['Student_Limit']) )

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

	#execute query to check the course
	course = fetch_all(CHECK_COURSE, request.form['Course_ID'])

	if (course):
		#execute query to add the section
		insert(CREATE_SECTION,(request.form['Section_ID'], request.form['Course_ID'], request.form['Course_Name'], request.form['Semester'], request.form['Section_Day'], request.form['Section_Time'], request.form['Student_Limit']) )

	else:
		#returns an error message to the html page
		error = 'Invalid Course ID'
		return render_template('AdminCreateSection.html', error=error)


	return redirect(url_for('AdminCreateSection'))


#Route for page with form to assign an instructor to a section
@app.route('/AssignInstructor')
def AssignInstructor():
	
	return render_template('AssignInstructor.html')


#assign professor to a section and update database function
@app.route('/InsertTeaches', methods=['GET', 'POST'])
def InsertTeaches():

	#execute query to fetch all details of the course
	course = fetch_all(CHECK_COURSE, request.form['Course_ID'])

	#execute query to fetch all details of the section
	section = fetch_all(CHECK_SECTION, (request.form['Section_ID'], request.form['Course_ID']))
	

	if (course and section): #Check if course and section exist
		#execute query to assign the instructor to teach
		insert(ASSIGN_INST, (request.form['Course_ID'], request.form['Instructor_ID'], request.form['Section_ID'] ))

	else: #if course or section dont exist
		error = 'Invalid Section'
		return render_template('AssignInstructor.html', error=error)

	return redirect(url_for('AssignInstructor'))


#Route for instrcutor page to create course
@app.route('/InstructorCreateCourse')
def InstructorCreateCourse():

	return render_template('InstructorCreateCourse.html')


#create and insert course into database function
@app.route('/InstructorInsertCourse', methods=['GET', 'POST'])
def InstructorInsertCourse():


	try:
		#execute query to add the course
		insert(CREATE_COURSE, (request.form['Course_ID'], request.form['Course_Name'], request.form['Course_Credits'], request.form['Course_Description'], request.form['Department_Name']))

		#execute query to add the section
		insert(CREATE_SECTION,(request.form['Section_ID'], request.form['Course_ID'], request.form['Course_Name'], request.form['Semester'], request.form['Section_Day'], request.form['Section_Time'], request.form['Student_Limit']) )

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

	#execute query to check if course exists
	course = fetch_all(CHECK_COURSE, request.form['Course_ID'])

	if (course):	#if the course exists then create section
		#execute query to add the section
		insert(CREATE_SECTION,(request.form['Section_ID'], request.form['Course_ID'], request.form['Course_Name'], request.form['Semester'], request.form['Section_Day'], request.form['Section_Time'], request.form['Student_Limit']))

	else:		# if course doesnt exist, return error message
		error = 'Invalid Course ID'
		return render_template('InstructorCreateSection.html', error=error)


	return redirect(url_for('InstructorCreateSection'))


#Route for admin page to create instructor account
@app.route('/CreateInstructor')
def CreateInstructor():
	
	return render_template('CreateInstructor.html')


#create and insert instructor into database 
@app.route('/InsertInstructor', methods=['GET', 'POST'])
def InsertInstructor():
	
	try:
		#execute query to add the instructor account
		insert(CREATE_INST, (request.form['Instructor_ID'], request.form['Instructor_Password'], request.form['Instructor_Fname'], request.form['Instructor_Lname'], request.form['Instructor_Email'], request.form['Department_Name']))

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

	try:
		#execute query to add the department
		insert(CREATE_DEPT, (request.form['Department_Name'], request.form['Department_Address'], request.form['Department_Email']))
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

	try:
		#execute query to add the admin account
		insert(CREATE_ADMIN, ( request.form['Admin_ID'], request.form['Admin_Password']))

		return redirect(url_for('CreateAdmin'))
	
	except Exception as e:		#if creating admin account fails return error
		conn.rollback()
		error = str(e)
		return render_template('CreateAdmin.html', error=error)



#page route and function for viewing the instructor's courses 
@app.route('/ViewInstructorCourses')
def ViewInstructorCourses():
	
	#Executes query to fetch details of all courses taught by this instructor
	teaches = fetch_all(INST_COURSES, session['Instructor_ID'])

	return render_template('InstructorCourses.html', teaches=teaches)



#page route and function for viewing the students in the instructor's chosen course
@app.route('/CourseStudents',methods=['GET', 'POST'])
def CourseStudents():
	
	if 'View_Students' in request.form:	#checks if instructor would like to view their courses
		
		# Course = request.form['View_Students']
		course=yaml.safe_load(request.form['View_Students'])
		

		#Executes query for getting students based on course and section ID and instructor teaching
		students = fetch_all(STUDENTS_ENROLLED, (course['Course_ID'], course['Section_ID'], session["Instructor_ID"]))
		
		return render_template('StudentsInCourse.html', students=students, Course_ID=course['Course_ID'])

	return redirect(url_for('ViewInstructorCourses'))



#page route and function for updating a students grade in the database
@app.route('/GradeStudents',methods=['GET', 'POST'])
def GradeStudents():
	
	if ('Confirm' in request.form):		#Check if instructor would like to update and fetches which student to assign grade to
		
		#Get grade value from instructor input to update database
		confirm = request.form['Confirm']
		

		confirm=yaml.safe_load(confirm)


		#Executes query for inserting student grade
		insert(UPDATE_GRADE, (request.form['Grade'],  confirm['Student_ID'], confirm['Section_ID'], confirm['Course_ID']))
		
	return redirect(url_for('CourseStudents'))



#Page route and function to fetch available sections for student registration based on course name
@app.route('/StudentSearchCourseName', methods=['GET', 'POST'])
def StudentSearchName():
	

	#Query to get available section information
	courses = fetch_all(SEARCH_CNAME,  request.form['Course_Name'])
	
	return render_template('StudentSearchCourseName.html',courses=courses)



#Page route and function to fetch courses for student registration based on department
@app.route('/StudentSearchDepartment', methods=['GET', 'POST'])
def StudentSearchDepartment():
	
	#Query to get available section information
	courses = fetch_all(SEARCH_CDEPT, request.form['Department_Name'])

	return render_template('StudentSearchDepartment.html',courses=courses)



#Page route and function to fetch courses for student registration based on instructor
@app.route('/StudentSearchInstructor', methods=['GET', 'POST'])
def StudentSearchInstructor():
	
	
	#Query to get available section information
	courses = fetch_all(SEARCH_CINST, request.form['Instructor_Name'])

	return render_template('StudentSearchInstructor.html',courses=courses)



#page route and function for adding a student to a section
@app.route('/Register', methods=['GET', 'POST'])
def Register():

	if ('Register' in request.form):		#Checks if student chose to register
		
		#Fetches data of which section is chosen
		register = request.form['Register']
		
		register=yaml.safe_load(register)
		
		try:
			#Executes query for inserting student into the section
			insert(ENROLL_STUDENT, (register['Course_ID'], session['Student_ID'], register['Section_ID']))

			#executes query to update student credits based on the registered course
			course_credits = fetch_one(GET_CREDITS,  register['Course_ID'])
			
			insert(UPDATE_CREDITS, course_credits['Course_Credits'])

		except Exception as e:		#if registering the student to the section fails return error

			conn.rollback()
			error = str(e)
			return render_template('CourseRegistrationSearch.html', error=error)
			
		
	return redirect('/StudentHome')


#page route for admin proposing the section choices to an instructor
@app.route('/ProposeChoice')
def ProposeChoice():

	return render_template('AdminProposeChoice.html')


#page route and function for admin proposing the section choices to an instructor in the database
@app.route('/InsertChoice', methods=['GET', 'POST'])
def InsertChoice():

	try:
		#execute query to add the choice to the database for instrcutor to choose
		insert(CREATE_CHOICE, (session['Admin_ID'], request.form['Instructor_ID'], request.form['Course_ID'], request.form['Course_Name'], request.form['Course_Credits'], request.form['Course_Description'], request.form['Department_Name'], request.form['Semester'], request.form['Student_Limit'], request.form['Section_ID'], request.form['Section_Day'], request.form['Section_Time'], request.form['Section2_ID'], request.form['Section2_Day'], request.form['Section2_Time']))
		
		return render_template('AdminProposeChoice.html')

	except Exception as e:		#if adding the choice fails returns error

		conn.rollback()
		error = str(e)

		return render_template('AdminProposeChoice.html', error=error)



#page route for instructor viewing proposed sections
@app.route('/ViewChoice')
def ViewChoice():

	#Fetches the most recent choice options for the instructor to choose
	line = fetch_one(FETCH_CHOICE, session['Instructor_ID'])

	return render_template('InstructorChoice.html', line= line)



#create and insert course and section based on instructor choice into database function
@app.route('/InsertSectionChoice', methods=['GET', 'POST'])
def InsertSectionChoice():

	course =  fetch_one(FETCH_CHOICE, session['Instructor_ID'])
	
	selected_section = request.form['Selected_Section']

	if (selected_section == 'Section1'):	#if chosen section is the first section
		
		#Query to create the new course
		insert(CREATE_COURSE, (course['Course_ID'], course['Course_Name'], course['Course_Credits'], course['Course_Description'], course['Department_Name']))

		#Query to create the new section
		insert(CREATE_SECTION, (course['Section_ID'], course['Course_ID'], course['Course_Name'], course['Semester'], course['Section_Day'], course['Section_Time'], course['Student_Limit']))

		#Query to assign the instructor to the new section
		insert(ASSIGN_INST, (course['Course_ID'], session['Instructor_ID'], course['Section_ID']))

		#Query to delete the choice options after the section is chosen and created
		insert(DELETE_CHOICE, (session['Instructor_ID'], course['Course_ID'], course['Section_ID'], course['Section2_ID']))



	elif (selected_section == 'Section2'):		#if chosen section is the second section

		#Query to create the new course
		insert(CREATE_COURSE, (course['Course_ID'], course['Course_Name'], course['Course_Credits'], course['Course_Description'], course['Department_Name']))

		#Query to create the new section
		insert(CREATE_SECTION, (course['Section2_ID'], course['Course_ID'], course['Course_Name'], course['Semester'], course['Section2_Day'], course['Section2_Time'], course['Student_Limit']))

		#Query to assign the instructor to the new section
		insert(ASSIGN_INST, (course['Course_ID'], session['Instructor_ID'], course['Section2_ID']))


		#Query to delete the choice options after the section is chosen and created
		insert(DELETE_CHOICE, (session['Instructor_ID'], course['Course_ID'], course['Section_ID'], course['Section2_ID']))



	return redirect('/InstructorHome')



app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)



