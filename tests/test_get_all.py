#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from constant2 import Constant


class Item(Constant):
    class Weapon(Constant):
        id = 1
        name = "weapon"
        weight = 10

    class Armor(Constant):
        id = 2
        name = "armor"
        weight = 10


item = Item()


class TestItem(object):
    """

    **中文文档**

    测试GetAll的排序功能是否有效。
    """

    def test_GetAll(self):
        assert Item.GetAll("weight", 10, sort_by="name") == [
            Item.Armor, Item.Weapon,
        ]

    def test_get_all(self):
        assert item.get_all("weight", 10, sort_by="name") == [
            item.Armor, item.Weapon,
        ]


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
