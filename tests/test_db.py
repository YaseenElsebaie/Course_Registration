import db

from queries import FETCH_COURSE_NAME


def test_fetch_all():
    assert db.fetch_all(FETCH_COURSE_NAME) is not None
