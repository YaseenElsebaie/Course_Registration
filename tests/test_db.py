import db

from queries import TEST_CREATE_DEPT2


def test_fetch_all():

    assert db.fetch_all("SELECT * FROM student") is not None

def test_fetch_all_empty():
    
    assert db.fetch_all("SELECT * FROM choice") == () 

def test_fetch_one():

    assert db.fetch_one("SELECT * FROM student") is not None

def test_fetch_one_empty():

    assert db.fetch_one("SELECT * FROM choice") is None 

def test_insert():
    assert db.insert(TEST_CREATE_DEPT2) is None

     
test_fetch_all()
test_fetch_all_empty()
test_fetch_one()
test_fetch_one_empty()
test_insert()
