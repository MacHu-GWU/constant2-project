#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import inspect
from copy import deepcopy
from pprint import pprint
from collections import OrderedDict
try:
    from .pkg.pylru import lrudecorator
    from .pkg.sixmini import integer_types, string_types, add_metaclass
    from .pkg.inspect_mate import (
        is_class_method, is_regular_method, get_all_attributes,
    )
    from .pkg.pytest import approx
    from .pkg.superjson import json
except:  # pragma: no cover
    from constant2.pkg.pylru import lrudecorator
    from constant2.pkg.sixmini import integer_types, string_types, add_metaclass
    from constant2.pkg.inspect_mate import (
        is_class_method, is_regular_method, get_all_attributes,
    )
    from constant2.pkg.pytest import approx
    from constant2.pkg.superjson import json

try:
    del json._dumpers["collections.OrderedDict"]
except KeyError:  # pragma: no cover
    pass

_reserved_attrs = set([
    "Items", "Keys", "Values",
    "items", "keys", "values",
    "ToDict", "to_dict",
    "Subclasses", "subclasses",
    "GetFirst", "get_first",
    "GetAll", "get_all",
    "dump", "load", "pprint", "jprint",
])


class Meta(type):
    """Meta class for :class:`Constant`.
    """
    def __new__(cls, name, bases, attrs):
        for attr, value in attrs.items():
            # nested class has to inherit from type or object
            # ``class MyClass:`` or ``class MyClass(object):``
            if inspect.isclass(value):
                # If it's inherit from type (in PY3) or object (in PY2)
                # inherit from Constant instead
                if isinstance(value, (type, object)):
                    kls = type(
                        value.__name__, (Constant,), value.__dict__.copy())
                    attrs[attr] = kls

        klass = super(Meta, cls).__new__(cls, name, bases, attrs)
        for attr in attrs:
            # Make sure reserved attributes are not been override
            if attr in _reserved_attrs:
                if not (is_class_method(klass, attr) or is_regular_method(klass, attr)):
                    raise AttributeError(
                        "%r is not a valid attribute name" % attr)

        return klass


@add_metaclass(Meta)
class Constant(object):
    """Generic Constantant.

    Inherit from this class to define a data container class.

    all nested Constant class automatically inherit from :class:`Constant`.
    """
    __creation_index__ = 0  # Used for sorting

    def __init__(self):
        """

        .. versionadded:: 0.0.3
        """
        for attr, value in self.__class__.Items():
            value = deepcopy(value)
            setattr(self, attr, value)

        for attr, Subclass in self.Subclasses():
            value = Subclass()
            setattr(self, attr, value)

        self.__creation_index__ = Constant.__creation_index__
        Constant.__creation_index__ += 1

    def __repr__(self):
        items_str = ", ".join(["%s=%r" % (attr, value)
                               for attr, value in self.items()])
        nested_str = ", ".join(
            ["%s=%r" % (attr, subclass) for attr, subclass in self.subclasses()])

        l = list()
        if items_str:
            l.append(items_str)

        if nested_str:
            l.append(nested_str)

        return "{classname}({args})".format(
            classname=self.__class__.__name__, args=", ".join(l))

    @classmethod
    def Items(cls):
        """non-class attributes ordered by alphabetical order.

        ::

            class MyClass(Constant):
                a = 1 # non-class attributre
                b = 2 # non-class attributre

                class C:
                    pass

                class D:
                    pass

        .. versionadded:: 0.0.5
        """
        l = list()
        for attr, value in get_all_attributes(cls):
            # if it's not a class(Constant)
            if not inspect.isclass(value):
                l.append((attr, value))

        return l

    def items(self):
        """non-class attributes ordered by alphabetical order.

        .. versionchanged:: 0.0.5
        """
        l = list()
        # 为什么这里是 get_all_attributes(self.__class__) 而不是
        # get_all_attributes(self) ? 因为有些实例不支持
        # get_all_attributes(instance) 方法, 会报错。
        # 所以我们从类里得到所有的属性信息, 然后获得这些属性在实例中
        # 对应的值。
        for attr, value in get_all_attributes(self.__class__):
            value = getattr(self, attr)

            # if it is not a instance of class(Constant)
            if not isinstance(value, Constant):
                l.append((attr, value))

        return l

    def __eq__(self, other):
        return self.items() == other.items()

    @classmethod
    def Keys(cls):
        """All non-class attribute name list.

        .. versionadded:: 0.0.5
        """
        return [attr for attr, _ in cls.Items()]

    def keys(self):
        """All non-class attribute name list.

        .. versionchanged:: 0.0.5
        """
        return [attr for attr, _ in self.items()]

    @classmethod
    def Values(cls):
        """All non-class attribute value list.

        .. versionadded:: 0.0.5
        """
        return [value for _, value in cls.Items()]

    def values(self):
        """All non-class attribute value list.

        .. versionchanged:: 0.0.5
        """
        return [value for _, value in self.items()]

    @classmethod
    def ToDict(cls):
        """Return regular class variable and it's value as a dictionary data.

        .. versionadded:: 0.0.5
        """
        return dict(cls.Items())

    def to_dict(self):
        """Return regular class variable and it's value as a dictionary data.

        .. versionchanged:: 0.0.5
        """
        return dict(self.items())

    @classmethod
    def Subclasses(cls, sort_by=None, reverse=False):
        """Get all nested Constant class and it's name pair.

        :param sort_by: the attribute name used for sorting.
        :param reverse: if True, return in descend order.
        :returns: [(attr, value),...] pairs.

        .. versionadded:: 0.0.3
        """
        l = list()
        for attr, value in get_all_attributes(cls):
            try:
                if issubclass(value, Constant):
                    l.append((attr, value))
            except:
                pass

        if sort_by is None:
            sort_by = "__creation_index__"

        l = list(
            sorted(l, key=lambda x: getattr(x[1], sort_by), reverse=reverse))

        return l

    def subclasses(self, sort_by=None, reverse=False):
        """Get all nested Constant class instance and it's name pair.

        :param sort_by: the attribute name used for sorting.
        :param reverse: if True, return in descend order.
        :returns: [(attr, value),...] pairs.

        .. versionadded:: 0.0.4
        """
        l = list()
        for attr, _ in self.Subclasses(sort_by, reverse):
            value = getattr(self, attr)
            l.append((attr, value))
        return l

    @classmethod
    @lrudecorator(size=32)
    def GetFirst(cls, attr, value, e=0.000001, sort_by="__name__"):
        """Get the first nested Constant class that met ``klass.attr == value``.

        :param attr: attribute name.
        :param value: value.
        :param e: used for float value comparison.
        :param sort_by: nested class is ordered by <sort_by> attribute.

        .. versionadded:: 0.0.5
        """
        for _, klass in cls.Subclasses(sort_by=sort_by):
            try:
                if klass.__dict__[attr] == approx(value, e):
                    return klass
            except:
                pass

        return None

    def get_first(self, attr, value, e=0.000001,
                  sort_by="__name__", reverse=False):
        """Get the first nested Constant class that met ``klass.attr == value``.

        :param attr: attribute name.
        :param value: value.
        :param e: used for float value comparison.
        :param sort_by: nested class is ordered by <sort_by> attribute.

        .. versionchanged:: 0.0.5
        """
        for _, klass in self.subclasses(sort_by, reverse):
            try:
                if getattr(klass, attr) == approx(value, e):
                    return klass
            except:
                pass

        return None

    @classmethod
    @lrudecorator(size=32)
    def GetAll(cls, attr, value, e=0.000001, sort_by="__name__"):
        """Get all nested Constant class that met ``klass.attr == value``.

        :param attr: attribute name.
        :param value: value.
        :param e: used for float value comparison.
        :param sort_by: nested class is ordered by <sort_by> attribute.

        .. versionadded:: 0.0.5
        """
        matched = list()
        for _, klass in cls.Subclasses(sort_by=sort_by):
            try:
                if klass.__dict__[attr] == approx(value, e):
                    matched.append(klass)
            except:  # pragma: no cover
                pass

        return matched

    def get_all(self, attr, value, e=0.000001,
                sort_by="__name__", reverse=False):
        """Get all nested Constant class that met ``klass.attr == value``.

        :param attr: attribute name.
        :param value: value.
        :param e: used for float value comparison.
        :param sort_by: nested class is ordered by <sort_by> attribute.

        .. versionchanged:: 0.0.5
        """
        matched = list()
        for _, klass in self.subclasses(sort_by, reverse):
            try:
                if getattr(klass, attr) == approx(value, e):
                    matched.append(klass)
            except:  # pragma: no cover
                pass

        return matched

    @classmethod
    def dump(cls):
        """Dump data into a dict.

        .. versionadded:: 0.0.2
        """
        d = OrderedDict(cls.Items())
        d["__classname__"] = cls.__name__
        for attr, klass in cls.Subclasses():
            d[attr] = klass.dump()
        return OrderedDict([(cls.__name__, d)])

    @classmethod
    def load(cls, data):
        """Construct a Constant class from it's dict data.

        .. versionadded:: 0.0.2
        """
        if len(data) == 1:
            for key, value in data.items():
                if "__classname__" not in value:  # pragma: no cover
                    raise ValueError
                name = key
                bases = (Constant, )
                attrs = dict()
                for k, v in value.items():
                    if isinstance(v, dict):
                        if "__classname__" in v:
                            attrs[k] = cls.load({k: v})
                        else:
                            attrs[k] = v
                    else:
                        attrs[k] = v
            return type(name, bases, attrs)
        else:  # pragma: no cover
            raise ValueError

    @classmethod
    def pprint(cls):  # pragma: no cover
        """Pretty print it's data.

        .. versionadded:: 0.0.2
        """
        pprint(cls.dump())

    @classmethod
    def jprint(cls):  # pragma: no cover
        """Json print it's data.

        .. versionadded:: 0.0.2
        """
        print(json.dumps(cls.dump(), pretty=4))


def is_same_dict(d1, d2):
    """Test two dictionary is equal on values. (ignore order)
    """
    for k, v in d1.items():
        if isinstance(v, dict):
            is_same_dict(v, d2[k])
        else:
            assert d1[k] == d2[k]

    for k, v in d2.items():
        if isinstance(v, dict):
            is_same_dict(v, d1[k])
        else:
            assert d1[k] == d2[k]


if __name__ == "__main__":

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
