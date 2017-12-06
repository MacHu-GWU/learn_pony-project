#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pony import orm

db = orm.Database()
db.bind(provider="sqlite", filename=":memory:")


class Person(db.Entity):
    id = orm.PrimaryKey(int)
    name = orm.Required(str)

    department = orm.Required(lambda: Department)
    tags = orm.Set(lambda: Tag)


class Department(db.Entity):
    id = orm.PrimaryKey(int)
    name = orm.Required(str)

    persons = orm.Set(lambda: Person)


class Tag(db.Entity):
    id = orm.PrimaryKey(int)
    name = orm.Required(str)

    persons = orm.Set(lambda: Person)


db.generate_mapping(create_tables=True)


@orm.db_session
def init_data():
    Python = Tag(id=1, name="Python")
    Java = Tag(id=2, name="Java")
    C = Tag(id=3, name="C")
    Payroll = Tag(id=4, name="Payroll")
    tags = [Python, Java, C, Payroll]

    dep_Manage = Department(id=1, name="Manage")
    dep_Finance = Department(id=2, name="Finance")
    dep_IT = Department(id=3, name="IT")
    depts = [dep_Manage, dep_Finance, dep_IT]

    Alice = Person(id=1, name="Alice", department=dep_Manage, tags=[])
    Bob = Person(id=2, name="Bob", department=dep_IT, tags=[Python, ])
    Cathy = Person(id=3, name="Cathy", department=dep_IT, tags=[Java, C])
    David = Person(id=4, name="David", department=dep_Finance, tags=[Payroll, ])
    persons = [Alice, Bob, Cathy, David]

    orm.commit()


init_data()


@orm.db_session
def test_query():
    query = (p for p in Person)
    for p in orm.select(query):
        assert isinstance(p.department, Department)
        for tag in p.tags:
            assert isinstance(tag, Tag)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
