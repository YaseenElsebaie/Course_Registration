
student_login = "SELECT Student_ID, Student_Password FROM Student WHERE Student_ID = %s and Student_Password = %s"


instructor_login = "SELECT Instructor_ID, Instructor_Password FROM Instructor WHERE Instructor_ID = %s and Instructor_Password = %s"


admin_login = "SELECT Admin_ID, Admin_Password FROM Instructor WHERE Admin_ID = %s and Admin_Password = %s"


register_student = "INSERT INTO Student (Student_ID, Student_Password, Student_Fname, Student_Lname, Major, Credits_Taken) VALUES (%s, %s,%s, %s, %s, %s)"


#	(Fetch Courses with specific name) 
fetch_course_name = "SELECT * FROM Course WHERE Course_Name=%s"

#	(Fetch Sections of that course)
fetch_section_name = "SELECT * FROM Section WHERE Course_Name=%s"


#	(Fetch Courses in department) 
fetch_course_dept = "SELECT * FROM Course WHERE Department_Name=%s"
#	(Fetch Sections of those courses) 
fetch_section_dept = "Select * FROM Section Natural Join Course WHERE Department_Name=%s"


#	(Fetch Courses based on instructor) 
fetch_course_inst = "SELECT * FROM Course Natural Join Section Natural Join Teaches Natural Join Instructor WHERE Instructor_Fname=%s"
#	(Fetch Sections of those courses) 
fetch_section_inst = "Select * FROM Teaches Natural Join Section Natural Join Instructor WHERE Instructor_Fname=%s"




#	(Fetch student info) 
fetch_student = "Select * from Student where Student_ID=%s"


#	To fetch and display all courses a student is taking
fetch_student_courses = "SELECT * FROM Takes Natural Join Course WHERE Student_ID=%s"


#	Student rates one of their courses
update_rating = "UPDATE Takes SET Rating = %s WHERE (Student_ID = %s) and (Section_ID = %s) and (Course_ID = %s)"


#	To fetch and display available sections searched by course name
#	(Fetch Sections and info with specific name and available capacity) 
search_cname = "SELECT * FROM Section Natural Join Instructor Natural Join Teaches Natural Join Course Natural Join coursesectioncapacitydiff where (Course_Name = %s) and (remaining_spots > 0)"


#	To fetch and display available sections under a specific department
#	(Fetch Sections and info in department and available capacity) 
search_cdept = "SELECT * FROM Section Natural Join Course Natural Join Instructor Natural Join Teaches Natural Join coursesectioncapacitydiff where (Department_Name = %s) and (remaining_spots > 0)"


#	To fetch and display available sections under a specific instructor
#	(Fetch Sections and info based on instructor and available capacity) 
search_cinst = "SELECT * FROM Section Natural Join Teaches Natural Join Instructor Natural Join coursesectioncapacitydiff where (Instructor_Fname = %s) and (remaining_spots > 0)"


#	(Insert Student into section) 
enroll_student = "INSERT INTO Takes (Course_ID, Student_ID, Section_ID) VALUES (%s, %s,%s)"
#	(Fetch Credits of course) 
fetch_course_credits = "Select Course_Credits from Course Where Course_ID = %s"
#	(Update student’s taken credits) 
update_credits = "Update Student SET Credits_Taken = Credits_Taken + %s"




#	(Fetch Instructor information) 
fetch_student = "Select * from Instructor where Instructor_ID=%s"


#	(Fetch instructor courses) 
fetch_inst_courses = "SELECT * FROM Teaches WHERE Instructor_ID=%s"


#	(Fetch students in the course) 
fetch_student_enrolled = "Select * from (Takes Natural Join Student Natural Join Teaches)  where (Course_ID = %s) and (Section_ID = %s) and (Instructor_ID = %s)"


#	(Insert/Update student’s grade) 
update_grade = "UPDATE Takes SET Grade = %s WHERE (Student_ID = %s) and (Section_ID = %s) and (Course_ID = %s)"


#	To create a course and a section

#	(Insert course) 
create_course = "INSERT INTO Course (Course_ID, Course_Name, Course_Credits, Course_Description, Department_Name ) VALUES (%s, %s,%s, %s, %s)"
#	(Insert Section) 
create_section = "INSERT INTO Section (Section_ID, Course_ID, Course_Name, Semester, Section_Day, Section_Time, Student_Limit ) VALUES (%s, %s,%s, %s, %s, %s, %s)"

#	To create a section for existing course
#	(Check if course exists) 
check_course = "Select * FROM Course Where Course_ID = %s"



#	To display choices of sections
#	(Fetch choice information) 
fetch_choice = "SELECT * FROM Choice where Instructor_ID = %s"


#	(Assign Instructor to chosen section) 
assign_inst = "Insert Into Teaches (Course_ID, Instructor_ID, Section_ID) VALUES (%s, %s, %s)"
#	(Delete choice entity from database) 
delete_choice = "DELETE FROM Choice WHERE Instructor_ID = %s AND Course_ID = %s AND Section_ID = %s AND Section2_ID = %s"




#	(Insert department) 
create_dept = "INSERT INTO Department (Department_Name, Department_Address, Department_Email) VALUES (%s, %s, %s)"


#	(Insert admin) 
create_admin = "INSERT INTO Administrator (Admin_ID, Admin_Password) VALUES (%s, %s)"


#	(Insert instructor) 
create_inst = "INSERT INTO Instructor (Instructor_ID, Instructor_Password, Instructor_Fname, Instructor_Lname, Instructor_Email, Department_Name) VALUES (%s, %s, %s, %s, %s, %s)"


#	To check if section exist
check_section = "Select * FROM Section Where Section_ID = %s and Course_ID = %s"


#	(Create Choice) 
create_choice = "INSERT INTO Choice (Admin_ID, Instructor_ID, Course_ID, Course_Name, Course_Credits, Course_Description, Department_Name, Semester, Student_Limit, Section_ID, Section_Day, Section_Time, Section2_ID, Section2_Day, Section2_Time) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s)"


