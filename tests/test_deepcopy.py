#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from constant2 import Constant


class Config(Constant):
    data = dict(a=1)

    class Setting(Constant):
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


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
