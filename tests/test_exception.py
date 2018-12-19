#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises
from constant2 import Constant


def test_reserved_method_error():
    with raises(AttributeError):
        class Dictionary(Constant):
            def keys(self):
                return iter(self)

    with raises(AttributeError):
        class Dictionary(Constant):
            keys = "a"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
