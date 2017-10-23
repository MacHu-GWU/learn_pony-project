#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pony solves N + 1 select problem very good.
"""

import pytest
from pony import orm

db = orm.Database()
db.bind(provider="sqlite", filename=":memory:")


class Customer(db.Entity):
    id = orm.PrimaryKey(int)
    name = orm.Required(str)
    orders = orm.Set(lambda: Order)


class Order(db.Entity):
    # id = orm.PrimaryKey(int)
    customer = orm.Required(Customer)


db.generate_mapping(create_tables=True)


@orm.db_session
def insert_test_data():
    customer1 = Customer(id=1, name="Alice")
    customer2 = Customer(id=2, name="Bob")
    customer3 = Customer(id=3, name="Cathy")

    order1 = Order(id=1, customer=customer1)
    order2 = Order(id=2, customer=customer2)
    order3 = Order(id=3, customer=customer3)
    order4 = Order(id=4, customer=customer1)
    order5 = Order(id=5, customer=customer1)

    orm.commit()


insert_test_data()


@orm.db_session
def test():
    query = orm.select(c for c in Customer)
    for c, n_order in zip(query, [3, 1, 1]):
        assert len(c.orders) == n_order


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
