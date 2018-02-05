#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from constant2 import Constant
from constant2._constant2 import is_same_dict


class User(Constant):
    id = None
    name = None


class AddressBook(Constant):
    alice = User
    bob = User


def test_different_attr_same_value():
    data = AddressBook.dump()

    data1 = {
        "AddressBook": {
            "__classname__": "AddressBook",
            "alice": {
                "User": {
                    "__classname__": "User",
                    "id": None,
                    "name": None,
                }
            },
            "bob": {
                "User": {
                    "__classname__": "User",
                    "id": None,
                    "name": None,
                }
            }
        }
    }
    is_same_dict(data, data1)

    ab = AddressBook()
    s = str(ab)
    assert "alice=User(id=None, name=None)" in s
    assert "bob=User(id=None, name=None)" in s


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
