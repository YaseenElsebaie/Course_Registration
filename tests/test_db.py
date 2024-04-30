import db

TEST_STUDENT_ID = "Y"
STUDENT_ID_FLD = "Student_ID" 
TEST_DEPT_NAME = "D8"
DEPT_NAME_FLD = "Department_Name"

def test_fetch_all():       #test to check if fetchall fetches correct type and value from database
    result = db.fetch_all("SELECT * FROM student")
    assert isinstance(result, list)
    assert len(result) > 0


def test_fetch_all_empty():     #test to check if fetchall fetches correct value if table is empty
    result = db.fetch_all("SELECT * FROM choice")
    assert result == () 


def test_fetch_one():       #test to check if fetchone fetches correct type and value from database
    query = f"SELECT * FROM student where Student_ID = '{TEST_STUDENT_ID}'"
    result = db.fetch_one(query)
    assert isinstance(result, dict)
    assert result[STUDENT_ID_FLD] == TEST_STUDENT_ID


def test_fetch_one_empty():         #test to check if fetchone fetches correct value if table is empty
    result = db.fetch_one("SELECT * FROM choice")
    assert result is None 



def test_insert():  #test to check if insertion runs correctly and inserts correct value
    insertion_bool  = db.run_query("INSERT INTO Department (Department_Name, Department_Address, Department_Email) "
                 + f"VALUES ('{TEST_DEPT_NAME}', '{TEST_DEPT_NAME}', '{TEST_DEPT_NAME}')")
    print(f"Insertion result: {insertion_bool}")
    
    if insertion_bool:
        result = db.fetch_one(f"Select * From Department where Department_Name = '{TEST_DEPT_NAME}'")
        assert isinstance(result, dict)
        assert result[DEPT_NAME_FLD] == TEST_DEPT_NAME
        print("Insertion Successful")
        db.run_query(f"DELETE FROM Department WHERE Department_Name = '{TEST_DEPT_NAME}' AND Department_Address = '{TEST_DEPT_NAME}' AND Department_Email = '{TEST_DEPT_NAME}'")
    elif not insertion_bool:    
        print("Insertion Failed")


def test_delete():          #test to check if deletion runs correctly and deletes correct value
    db.run_query("INSERT INTO Department (Department_Name, Department_Address, Department_Email) "
                 + f"VALUES ('{TEST_DEPT_NAME}', '{TEST_DEPT_NAME}', '{TEST_DEPT_NAME}')")
    deletion_bool = db.run_query(f"DELETE FROM Department WHERE Department_Name = '{TEST_DEPT_NAME}' AND Department_Address = '{TEST_DEPT_NAME}' AND Department_Email = '{TEST_DEPT_NAME}' ")
    print(f"Deletion result: {deletion_bool}")

    if (deletion_bool):
        result = db.fetch_one(f"Select * From Department where Department_Name = '{TEST_DEPT_NAME}' AND Department_Address = '{TEST_DEPT_NAME}' AND Department_Email = '{TEST_DEPT_NAME}'")
        assert result is None
    else:
        print("Deletion Failed") 



     
     
