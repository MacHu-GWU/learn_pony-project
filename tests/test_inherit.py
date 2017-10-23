#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pony use another column "classtype" to indicate class type for inheritance
implementation.
"""

import pytest
from pony import orm

db = orm.Database()
db.bind(provider="sqlite", filename=":memory:")


class Person(db.Entity):
    id = orm.PrimaryKey(int)
    name = orm.Required(str)


class Student(Person):
    pass


class Teacher(Person):
    pass


class TeachingAssistance(Student, Teacher):
    pass


db.generate_mapping(create_tables=True)


@orm.db_session
def insert_test_data():
    person1 = Person(id=1, name="Alice")
    student2 = Student(id=2, name="Bob")
    teacher3 = Teacher(id=3, name="Cathy")
    ta4 = TeachingAssistance(id=4, name="David")
    orm.commit()


insert_test_data()


@orm.db_session
def test():
    for p in orm.select(p for p in Person):
        assert "classtype" in p.to_dict()

    for p in orm.select(p for p in Student):
        assert "classtype" in p.to_dict()

    for p in orm.select(p for p in Teacher):
        assert "classtype" in p.to_dict()

    for p in orm.select(p for p in TeachingAssistance):
        assert "classtype" in p.to_dict()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
