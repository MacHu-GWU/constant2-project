#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.1"
__short_description__ = "provide extensive way of managing your constant variable."
__license__ = "MIT"
__author__ = "Sanhe Hu"


import inspect
try:
    from .pkg.pylru import lrudecorator
    from .pkg.sixmini import integer_types, string_types, add_metaclass
    from .pkg.inspect_mate import is_class_method, get_all_attributes
    from .pkg.pytest import approx
except:
    from constant2.pkg.pylru import lrudecorator
    from constant2.pkg.sixmini import integer_types, string_types, add_metaclass
    from constant2.pkg.inspect_mate import is_class_method, get_all_attributes
    from constant2.pkg.pytest import approx


_reserved_attrs = set([
    "items", "keys", "values", "nested", "get_first", "get_all",
])


class Meta(type):
    """Meta class for :class:`Constant`.
    """
    def __new__(cls, name, bases, attrs):
        for attr, value in attrs.items():
            # Make sure reserved attributes are not been override
            if attr in _reserved_attrs:
                if not isinstance(value, classmethod):
                    raise AttributeError(
                        "%r is not a valid attribute name" % attr)

            # nested class has to inherit from type or object
            # ``class MyClass:`` or ``class MyClass(object):``
            if inspect.isclass(value):
                if isinstance(value, (type, object)):
                    kls = type(value.__name__, (Constant,), value.__dict__.copy())
                    attrs[attr] = kls

        klass = super(Meta, cls).__new__(cls, name, bases, attrs)
        return klass


@add_metaclass(Meta)
class Constant(object):
    """Generic Constantant.

    Inherit from this class to define a data container class.

    all nested Constant class automatically inherit from :class:`Constant`. 
    """
    @classmethod
    def items(cls):
        """non-class attributes ordered by alphabetical order.
        """
        l = list()
        for attr, value in get_all_attributes(cls):
            try:
                if not issubclass(value, Constant):
                    l.append((attr, value))
            except:
                l.append((attr, value))
        return l

    @classmethod
    def keys(cls):
        """All non-class attribute name list. 
        """
        return [attr for attr, _ in cls.items()]

    @classmethod
    def values(cls):
        """All non-class attribute value list.
        """
        return [value for _, value in cls.items()]

    @classmethod
    def to_dict(cls):
        """Return regular class variable and it's value as a dictionary data.
        """
        return dict(cls.items())

    @classmethod
    def nested(cls, sort_by=None, reverse=False):
        """Get all nested Constant class, in alphabetical order.
        """
        l = list()
        for attr, value in get_all_attributes(cls):
            try:
                if issubclass(value, Constant):
                    l.append(value)
            except:
                pass
        if sort_by is not None:
            l = list(
                sorted(l, key=lambda x: getattr(x, sort_by), reverse=reverse))
        return l

    @classmethod
    @lrudecorator(size=32)
    def get_first(cls, attr, value, e=0.000001, sort_by="__name__"):
        """Get the first nested Constantant class that met ``klass.attr == value``.

        :param attr: attribute name.
        :param value: value.
        :param e: used for float value comparison.
        :param sort_by: nested class is ordered by <sort_by> attribute.
        """
        for klass in cls.nested(sort_by=sort_by):
            try:
                if klass.__dict__[attr] == approx(value, e):
                    return klass
            except:
                pass

        return None

    @classmethod
    @lrudecorator(size=32)
    def get_all(cls, attr, value, e=0.000001, sort_by="__name__"):
        """Get all nested Constantant class that met ``klass.attr == value``.

        :param attr: attribute name.
        :param value: value.
        :param e: used for float value comparison.
        :param sort_by: nested class is ordered by <sort_by> attribute.
        """
        matched = list()
        for klass in cls.nested(sort_by=sort_by):
            try:
                if klass.__dict__[attr] == approx(value, e):
                    matched.append(klass)
            except:
                pass

        return matched


if __name__ == "__main__":
    class Food(Constant):

        class Fruit:
            id = 1
            name = "fruit"

    # print(Food.items())

#             class Apple:
#                 id = 1
#                 name = "apple"
#
#                 class RedApple:
#                     id = 1
#                     name = "red apple"
#
#                 class GreenApple:
#                     id = 2
#                     name = "green apple"
#
#             class Banana:
#                 id = 2
#                 name = "banana"
#
#                 class YellowBanana:
#                     id = 1
#                     name = "yellow banana"
#
#                 class GreenBanana:
#                     id = 2
#                     name = "green banana"
#
#         class Meat:
#             id = 2
#             name = "meat"
#
#             class Pork:
#                 id = 1
#                 name = "pork"
#
#             class Meat:
#                 id = 2
#                 name = "meat"
