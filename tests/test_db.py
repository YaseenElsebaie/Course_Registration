import db

from queries import FETCH_COURSE_NAME
from queries import enroll_student


def test_fetch_all():
    assert db.fetch_all(FETCH_COURSE_NAME) is not None

def test_fetch_one():
    assert db.fetch_one(FETCH_COURSE_NAME) is not None

def test_insert():
     assert db.insert(enroll_student)

     
test_fetch_all()
test_fetch_one()
test_insert()
