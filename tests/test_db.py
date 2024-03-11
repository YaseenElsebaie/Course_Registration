import db

from queries import FETCH_COURSE_NAME
from queries import CREATE_DEPT2


def test_fetch_all():

    assert db.fetch_all("SELECT * FROM student") is not None

    assert db.fetch_all("SELECT * FROM test") is None

def test_fetch_one():

    assert db.fetch_one("SELECT * FROM student") is not None

    assert db.fetch_one("SELECT * FROM test") is None

def test_insert():
     assert db.insert(CREATE_DEPT2)

     
test_fetch_all()
test_fetch_one()
test_insert()
