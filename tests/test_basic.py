#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test:

- MyClass.Items()
- MyClass.Keys()
- MyClass.Values()
- MyClass.Subclasses()
- my_class.items()
- my_class.keys()
- my_class.values()
- my_class.subclass()
"""

import time
import pytest
from constant2 import Constant
from constant2._constant2 import is_same_dict


class Food(Constant):
    class Fruit(Constant):
        id = 1
        name = "fruit"

        class Apple(Constant):
            id = 1
            name = "apple"

            class RedApple(Constant):
                id = 1
                name = "red apple"

            class GreenApple(Constant):
                id = 2
                name = "green apple"

        class Banana(Constant):
            id = 2
            name = "banana"

            class YellowBanana(Constant):
                id = 1
                name = "yellow banana"

            class GreenBanana(Constant):
                id = 2
                name = "green banana"

    class Meat(Constant):
        id = 2
        name = "meat"

        class Pork(Constant):
            id = 1
            name = "pork"

        class Beef(Constant):
            id = 2
            name = "beef"


food = Food()


class TestFood(object):
    def test_Items(self):
        assert Food.Items() == []
        assert Food.Fruit.Items() == [("id", 1), ("name", "fruit")]
        assert Food.Fruit.Apple.Items() == [("id", 1), ("name", "apple")]
        assert Food.Fruit.Apple.RedApple.Items() == [
            ("id", 1), ("name", "red apple"),
        ]

        assert Food.Keys() == []
        assert Food.Fruit.Keys() == ["id", "name"]
        assert Food.Fruit.Apple.Keys() == ["id", "name"]
        assert Food.Fruit.Apple.RedApple.Keys() == ["id", "name"]

        assert Food.Values() == []
        assert Food.Fruit.Values() == [1, "fruit"]
        assert Food.Fruit.Apple.Values() == [1, "apple"]
        assert Food.Fruit.Apple.RedApple.Values() == [1, "red apple"]

    def test_items(self):
        assert food.items() == []
        assert food.Fruit.items() == [("id", 1), ("name", "fruit")]
        assert food.Fruit.Apple.items() == [("id", 1), ("name", "apple")]
        assert food.Fruit.Apple.RedApple.items() == [
            ("id", 1), ("name", "red apple"),
        ]

        assert food.keys() == []
        assert food.Fruit.keys() == ["id", "name"]
        assert food.Fruit.Apple.keys() == ["id", "name"]
        assert food.Fruit.Apple.RedApple.keys() == ["id", "name"]

        assert food.values() == []
        assert food.Fruit.values() == [1, "fruit"]
        assert food.Fruit.Apple.values() == [1, "apple"]
        assert food.Fruit.Apple.RedApple.values() == [1, "red apple"]

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
        # print("with lfu_cache elapsed %.6f second." % elapsed)

    def test_get_first_performance(self):
        st = time.clock()
        for i in range(1000):
            food.get_first("id", 2)
        elapsed = time.clock() - st
        # print("without lfu_cache elapsed %.6f second." % elapsed)

    def test_ToIds(self):
        assert Food.ToIds([Food.Fruit, Food.Meat]) == [1, 2]

    def test_to_ids(self):
        assert food.to_ids([food.Fruit, food.Meat]) == [1, 2]

    def test_ToClasses(self):
        assert Food.ToClasses([1, 2]) == [Food.Fruit, Food.Meat]

    def test_to_instances(self):
        assert food.to_instances([1, 2]) == [food.Fruit, food.Meat]

    def test_SubIds(self):
        assert Food.SubIds() == [1, 2]

    def test_sub_ids(self):
        assert food.sub_ids() == [1, 2]

    def test_ToDict(self):
        assert Food.ToDict() == {}
        assert Food.Fruit.ToDict() == {"id": 1, "name": "fruit"}

    def test_to_dict(self):
        assert food.to_dict() == {}
        assert food.Fruit.to_dict() == {"id": 1, "name": "fruit"}

    def test_dump_load(self):
        data = Food.dump()
        Food1 = Constant.load(data)
        data1 = Food1.dump()
        is_same_dict(data, data1)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
