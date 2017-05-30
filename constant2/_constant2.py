#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import inspect
from pprint import pprint
from collections import OrderedDict
try:
    from .pkg.pylru import lrudecorator
    from .pkg.sixmini import integer_types, string_types, add_metaclass
    from .pkg.inspect_mate import is_class_method, get_all_attributes
    from .pkg.pytest import approx
    from .pkg.superjson import json
except:
    from constant2.pkg.pylru import lrudecorator
    from constant2.pkg.sixmini import integer_types, string_types, add_metaclass
    from constant2.pkg.inspect_mate import is_class_method, get_all_attributes
    from constant2.pkg.pytest import approx
    from constant2.pkg.superjson import json
    
try:
    del json._dumpers["collections.OrderedDict"]
except KeyError:
    pass

_reserved_attrs = set([
    "items", "keys", "values", "nested", "get_first", "get_all",
    "dump", "load", "pprint", "jprint",
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
                    kls = type(
                        value.__name__, (Constant,), value.__dict__.copy())
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

    @classmethod
    def dump(cls):
        """Dump data into a dict.
        
        .. versionadded:: 0.0.2
        """
        d = OrderedDict(cls.items())
        d["__classname__"] = cls.__name__
        for klass in cls.nested():
            d.update(klass.dump())
        return OrderedDict([(cls.__name__, d)])

    @classmethod
    def load(cls, data):
        """Construct a Constant class from it's dict data.
        
        .. versionadded:: 0.0.2
        """
        if len(data) == 1:
            for key, value in data.items():
                if "__classname__" not in value:
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
        else:
            raise ValueError

    @classmethod
    def pprint(cls):
        """Pretty print it's data.
        
        .. versionadded:: 0.0.2
        """
        pprint(cls.dump())

    @classmethod
    def jprint(cls):
        """Json print it's data.
        
        .. versionadded:: 0.0.2
        """
        print(json.dumps(cls.dump(), pretty=True))


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
                
    Food.jprint()
