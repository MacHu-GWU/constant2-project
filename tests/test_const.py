#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unittest
"""

from __future__ import print_function
import pytest
from constant2 import Constant
from constant2._constant2 import is_same_dict


class Food(Constant):

    class Fruit:
        id = 1
        name = "fruit"

        class Apple:
            id = 1
            name = "apple"

            class RedApple:
                id = 1
                name = "red apple"

            class GreenApple:
                id = 2
                name = "green apple"

        class Banana:
            id = 2
            name = "banana"

            class YellowBanana:
                id = 1
                name = "yellow banana"

            class GreenBanana:
                id = 2
                name = "green banana"

    class Meat:
        id = 2
        name = "meat"

        class Pork:
            id = 1
            name = "pork"

        class Beef:
            id = 2
            name = "beef"


class Item(Constant):

    class Weapon:
        id = 1
        name = "weapon"
        weight = 10

    class Armor:
        id = 2
        name = "armor"
        weight = 10


def test_items():
    assert Food.items() == []
    assert Food.Fruit.items() == [("id", 1), ("name", "fruit")]
    assert Food.Fruit.Apple.items() == [("id", 1), ("name", "apple")]
    assert Food.Fruit.Apple.RedApple.items(
    ) == [("id", 1), ("name", "red apple")]


def test_nested():
    assert Food.nested() == [Food.Fruit, Food.Meat]
    assert Food.Fruit.nested() == [Food.Fruit.Apple, Food.Fruit.Banana]
    assert Food.Fruit.Apple.nested(
        sort_by="__name__") == [Food.Fruit.Apple.GreenApple, Food.Fruit.Apple.RedApple]
    assert Food.Fruit.Apple.nested(
        sort_by="name") == [Food.Fruit.Apple.GreenApple, Food.Fruit.Apple.RedApple]
    assert Food.Fruit.Apple.nested(
        sort_by="id") == [Food.Fruit.Apple.RedApple, Food.Fruit.Apple.GreenApple]
    assert Food.Fruit.Apple.nested(sort_by="id", reverse=True) == [
        Food.Fruit.Apple.GreenApple, Food.Fruit.Apple.RedApple]
    assert Food.Fruit.Apple.RedApple.nested() == []


def test_get_first():
    assert Food.get_first("id", 1) == Food.Fruit
    assert Food.get_first("name", "meat") == Food.Meat
    assert Food.get_first("value", "Hello World") is None


def test_get_first_performance():
    import time

    st = time.clock()
    for i in range(1000):
        Food.get_first("id", 2)
    elapsed = time.clock() - st
    print("with lfu_cache elapsed %.6f second." % elapsed)


def test_get_all():
    assert Item.get_all("weight", 10, sort_by="id") == [
        Item.Weapon, Item.Armor]


def test_dump_load():
    data = Food.dump()
    Food1 = Constant.load(data)
    data1 = Food1.dump()
    is_same_dict(data, data1)


class Config(Constant):
    data = dict(a=1)

    class Setting:
        data = dict(a=1)


def test_instance_deepcopy():
    config1 = Config()
    config1.data["a"] = 2
    config1.Setting.data["a"] = 2

    config2 = Config()
    assert config2.data["a"] == 1
    assert config2.Setting.data["a"] == 1


class User:
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
    assert "alice" in s
    assert "bob" in s


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
