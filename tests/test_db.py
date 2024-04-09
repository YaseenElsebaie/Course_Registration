import db

TEST_STUDENT_ID = "Y"
STUDENT_ID_FLD = "Student_ID" 

def test_fetch_all():
    result = db.fetch_all("SELECT * FROM student")
    assert isinstance(result, list)
    assert len(result) > 0


def test_fetch_all_empty():
    result = db.fetch_all("SELECT * FROM choice")
    assert result == () 


def test_fetch_one():
    query = f"SELECT * FROM student where Student_ID = '{TEST_STUDENT_ID}'"
    result = db.fetch_one(query)
    assert isinstance(result, dict)
    assert result[STUDENT_ID_FLD] == TEST_STUDENT_ID


def test_fetch_one_empty():
    result = db.fetch_one("SELECT * FROM choice")
    assert result is None 


def test_insert():
    result = db.insert("INSERT INTO Department (Department_Name, Department_Address, Department_Email) VALUES ('D8', 'D8', 'D8')")
    assert result is None


def test_delete():
    result = db.insert("DELETE FROM Department WHERE Department_Name = 'D8' AND Department_Address = 'D8' AND Department_Email = 'D8' ")
    assert result is None

     
