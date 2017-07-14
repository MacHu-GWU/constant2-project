#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unittest
"""

from __future__ import print_function
import time
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


food = Food()


class TestFood:

    def test_Items(self):
        assert Food.Items() == []
        assert Food.Fruit.Items() == [("id", 1), ("name", "fruit")]
        assert Food.Fruit.Apple.Items() == [("id", 1), ("name", "apple")]
        assert Food.Fruit.Apple.RedApple.Items() == [
            ("id", 1), ("name", "red apple"),
        ]

    def test_items(self):
        assert Food.Items() == []
        assert Food.Fruit.Items() == [("id", 1), ("name", "fruit")]
        assert Food.Fruit.Apple.Items() == [("id", 1), ("name", "apple")]
        assert Food.Fruit.Apple.RedApple.Items() == [
            ("id", 1), ("name", "red apple"),
        ]

    def test_Subclass(self):
        assert Food.Subclasses() == [
            ("Fruit", Food.Fruit),
            ("Meat", Food.Meat),
        ]

        assert Food.Fruit.Subclasses() == [
            ("Apple", Food.Fruit.Apple),
            ("Banana", Food.Fruit.Banana),
        ]

        assert Food.Fruit.Apple.Subclasses(sort_by="__name__") == [
            ("GreenApple", Food.Fruit.Apple.GreenApple),
            ("RedApple", Food.Fruit.Apple.RedApple),
        ]

        assert Food.Fruit.Apple.Subclasses(sort_by="id") == [
            ("RedApple", Food.Fruit.Apple.RedApple),
            ("GreenApple", Food.Fruit.Apple.GreenApple),
        ]

        assert Food.Fruit.Apple.RedApple.Subclasses() == []

    def test_subclass(self):
        assert food.subclasses() == [
            ("Fruit", food.Fruit), ("Meat", food.Meat)]

        assert food.Fruit.subclasses() == [
            ("Apple", food.Fruit.Apple), ("Banana", food.Fruit.Banana),
        ]

        assert food.Fruit.Apple.subclasses(sort_by="__name__") == [
            ("GreenApple", food.Fruit.Apple.GreenApple),
            ("RedApple", food.Fruit.Apple.RedApple),
        ]

        assert food.Fruit.Apple.subclasses(sort_by="id") == [
            ("RedApple", food.Fruit.Apple.RedApple),
            ("GreenApple", food.Fruit.Apple.GreenApple),
        ]

    def test_GetFirst(self):
        assert Food.GetFirst("id", 1) == Food.Fruit
        assert Food.GetFirst("name", "meat") == Food.Meat
        assert Food.GetFirst("value", "Hello World") is None

    def test_get_first(self):
        assert food.get_first("id", 1) == food.Fruit
        assert food.get_first("name", "meat") == food.Meat
        assert food.get_first("value", "Hello World") is None

    def test_GetFirst_performance(self):
        st = time.clock()
        for i in range(1000):
            Food.GetFirst("id", 2)
        elapsed = time.clock() - st
        print("with lfu_cache elapsed %.6f second." % elapsed)

    def test_get_first_performance(self):
        st = time.clock()
        for i in range(1000):
            food.get_first("id", 2)
        elapsed = time.clock() - st
        print("without lfu_cache elapsed %.6f second." % elapsed)

    def test_dump_load(self):
        data = Food.dump()
        Food1 = Constant.load(data)
        data1 = Food1.dump()
        is_same_dict(data, data1)


class Item(Constant):

    class Weapon:
        id = 1
        name = "weapon"
        weight = 10

    class Armor:
        id = 2
        name = "armor"
        weight = 10


item = Item()


class TestItem:

    def test_GetAll(self):
        assert Item.GetAll("weight", 10, sort_by="name") == [
            Item.Armor, Item.Weapon,
        ]

    def test_get_all(self):
        assert item.get_all("weight", 10, sort_by="name") == [
            item.Armor, item.Weapon,
        ]


class Config(Constant):
    data = dict(a=1)

    class Setting:
        data = dict(a=1)


def test_instance_deepcopy():
    """Although, if the attribute of the class is mutable object.

    Edit it's value on one instance will not affect other instance and the 
    original class.
    """
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
    assert "alice=User(id=None, name=None)" in s
    assert "bob=User(id=None, name=None)" in s


if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])
