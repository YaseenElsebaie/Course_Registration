
STUDENT_LOGIN = "SELECT Student_ID, Student_Password FROM Student WHERE Student_ID = %s and Student_Password = %s"
STUDENT_INFO = "Select * from Student where Student_ID=%s"

INST_LOGIN = "SELECT Instructor_ID, Instructor_Password FROM Instructor WHERE Instructor_ID = %s and Instructor_Password = %s"
INST_INFO = "Select * from Instructor where Instructor_ID=%s"

ADMIN_LOGIN = "SELECT Admin_ID, Admin_Password FROM Administrator WHERE Admin_ID = %s and Admin_Password = %s"


REGISTER_STUDENT = "INSERT INTO Student (Student_ID, Student_Password, Student_Fname, Student_Lname, Major, Credits_Taken) VALUES (%s, %s,%s, %s, %s, %s)"


#	(Fetch Courses with specific name) 
FETCH_COURSE_NAME = "SELECT * FROM Course WHERE Course_Name=%s"


#	(Fetch Sections of that course)
FETCH_SECTION_NAME = "SELECT * FROM Section WHERE Course_Name=%s"


#	(Fetch Courses in department) 
FETCH_COURSE_DEPT = "SELECT * FROM Course WHERE Department_Name=%s"
#	(Fetch Sections of those courses) 
FETCH_SECTION_DEPT = "Select * FROM Section Natural Join Course WHERE Department_Name=%s"


#	(Fetch Courses based on instructor) 
FETCH_COURSE_INST = "SELECT * FROM Course Natural Join Section Natural Join Teaches Natural Join Instructor WHERE Instructor_Fname=%s"
#	(Fetch Sections of those courses) 
FETCH_SECTION_INST = "Select * FROM Teaches Natural Join Section Natural Join Instructor WHERE Instructor_Fname=%s"




#	(Fetch student info) 
FETCH_STUDENT = "Select * from Student where Student_ID=%s"


#	To fetch and display all courses a student is taking
FETCH_STUDENT_COURSES = "SELECT * FROM Takes Natural Join Course WHERE Student_ID=%s"


#	Student rates one of their courses
UPDATE_RATING = "UPDATE Takes SET Rating = %s WHERE (Student_ID = %s) and (Section_ID = %s) and (Course_ID = %s)"


#	To fetch and display available sections searched by course name
#	(Fetch Sections and info with specific name and available capacity) 
SEARCH_CNAME = "SELECT * FROM Section Natural Join Instructor Natural Join Teaches Natural Join Course Natural Join coursesectioncapacitydiff where (Course_Name = %s) and (remaining_spots > 0)"


#	To fetch and display available sections under a specific department
#	(Fetch Sections and info in department and available capacity) 
SEARCH_CDEPT = "SELECT * FROM Section Natural Join Course Natural Join Instructor Natural Join Teaches Natural Join coursesectioncapacitydiff where (Department_Name = %s) and (remaining_spots > 0)"


#	To fetch and display available sections under a specific instructor
#	(Fetch Sections and info based on instructor and available capacity) 
SEARCH_CINST = "SELECT * FROM Section Natural Join Teaches Natural Join Instructor Natural Join coursesectioncapacitydiff where (Instructor_Fname = %s) and (remaining_spots > 0)"


#	(Insert Student into section) 
ENROLL_STUDENT = "INSERT INTO Takes (Course_ID, Student_ID, Section_ID) VALUES (%s, %s,%s)"
#	(Fetch Credits of course) 
GET_CREDITS = "Select Course_Credits from Course Where Course_ID = %s"
#	(Update student’s taken credits) 
UPDATE_CREDITS = "Update Student SET Credits_Taken = Credits_Taken + %s"




#	(Fetch Instructor information) 
FETCH_INST = "Select * from Instructor where Instructor_ID=%s"


#	(Fetch instructor courses) 
INST_COURSES = "SELECT * FROM Teaches WHERE Instructor_ID=%s"


#	(Fetch students in the course) 
STUDENTS_ENROLLED = "Select * from (Takes Natural Join Student Natural Join Teaches)  where (Course_ID = %s) and (Section_ID = %s) and (Instructor_ID = %s)"


#	(Insert/Update student’s grade) 
UPDATE_GRADE = "UPDATE Takes SET Grade = %s WHERE (Student_ID = %s) and (Section_ID = %s) and (Course_ID = %s)"


#	To create a course and a section

#	(Insert course) 
CREATE_COURSE = "INSERT INTO Course (Course_ID, Course_Name, Course_Credits, Course_Description, Department_Name ) VALUES (%s, %s,%s, %s, %s)"
#	(Insert Section) 
CREATE_SECTION = "INSERT INTO Section (Section_ID, Course_ID, Course_Name, Semester, Section_Day, Section_Time, Student_Limit ) VALUES (%s, %s,%s, %s, %s, %s, %s)"

#	To create a section for existing course
#	(Check if course exists) 
CHECK_COURSE = "Select * FROM Course Where Course_ID = %s"



#	To display choices of sections
#	(Fetch choice information) 
FETCH_CHOICE = "SELECT * FROM Choice where Instructor_ID = %s"


#	(Assign Instructor to chosen section) 
ASSIGN_INST = "Insert Into Teaches (Course_ID, Instructor_ID, Section_ID) VALUES (%s, %s, %s)"
#	(Delete choice entity from database) 
DELETE_CHOICE = "DELETE FROM Choice WHERE Instructor_ID = %s AND Course_ID = %s AND Section_ID = %s AND Section2_ID = %s"




#	(Insert department) 
CREATE_DEPT = "INSERT INTO Department (Department_Name, Department_Address, Department_Email) VALUES (%s, %s, %s)"


#	(Insert admin) 
CREATE_ADMIN = "INSERT INTO Administrator (Admin_ID, Admin_Password) VALUES (%s, %s)"


#	(Insert instructor) 
CREATE_INST = "INSERT INTO Instructor (Instructor_ID, Instructor_Password, Instructor_Fname, Instructor_Lname, Instructor_Email, Department_Name) VALUES (%s, %s, %s, %s, %s, %s)"


#	To check if section exist
CHECK_SECTION = "Select * FROM Section Where Section_ID = %s and Course_ID = %s"


#	(Create Choice) 
CREATE_CHOICE = "INSERT INTO Choice (Admin_ID, Instructor_ID, Course_ID, Course_Name, Course_Credits, Course_Description, Department_Name, Semester, Student_Limit, Section_ID, Section_Day, Section_Time, Section2_ID, Section2_Day, Section2_Time) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s)"
