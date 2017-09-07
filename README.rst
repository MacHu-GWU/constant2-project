.. image:: https://travis-ci.org/MacHu-GWU/constant2-project.svg?branch=master
    :target: https://travis-ci.org/MacHu-GWU/constant2-project?branch=master

.. image:: https://codecov.io/gh/MacHu-GWU/constant2-project/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/MacHu-GWU/constant2-project

.. image:: https://img.shields.io/pypi/v/constant2.svg
    :target: https://pypi.python.org/pypi/constant2

.. image:: https://img.shields.io/pypi/l/constant2.svg
    :target: https://pypi.python.org/pypi/constant2

.. image:: https://img.shields.io/pypi/pyversions/constant2.svg
    :target: https://pypi.python.org/pypi/constant2

.. image:: https://img.shields.io/badge/Star_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/constant2-project


Welcome to ``constant2`` Documentation
==============================================================================

If you have lots of constant2 value widely used across your development. A better way is to define ``Constantant Variable`` rather than using the raw value. This can improve the readability.

``constant2`` is a library provide extensive way of managing your constant2 variable.


Quick Links
-----------
- `GitHub Homepage <https://github.com/MacHu-GWU/constant2-project>`_
- `Online Documentation <http://www.wbh-doc.com.s3.amazonaws.com/constant2/index.html>`_
- `PyPI download <https://pypi.python.org/pypi/constant2>`_
- `Install <install_>`_
- `Issue submit and feature request <https://github.com/MacHu-GWU/constant2-project/issues>`_
- `API reference and source code <http://www.wbh-doc.com.s3.amazonaws.com/constant2/py-modindex.html>`_


Usage
-----

.. code-block:: python

    from constant2 import Constant

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

You can visit it's data or child class data in these way:

.. code-block:: python

    # Use class
    >>> Fruit.Items() # .Items() return it's data
    [('id', 1), ('name', 'fruit')]

    >>> Fruit.Keys() # .Keys() return keys
    ['id', 'name']

    >>> Fruit.Values() # .Values() return values
    [1, 'fruit']

    >>> Fruit.ToDict() # return data in a dict
    {'id': 1, 'name': 'fruit'}

    # use instance
    >>> food.items() # .Items() return it's data
    [('id', 1), ('name', 'fruit')]

    >>> food.keys() # .keys() return keys
    ['id', 'name']

    >>> food.values() # .values() return values
    [1, 'fruit']

    >>> food.to_dict() # return data in a dict
    {'id': 1, 'name': 'fruit'}

    # iterate on all nested class
    >>> Fruit.Subclasses(sort_by='id')
    [class Apple, class Banana]

    # get first nested class that kls.id == 1
    # useful when you need reverse lookup
    >>> Fruit.GetFirst('id', 1)
    class Apple

    # get all child class that kls.id == 1
    >>> Fruit.GetAll('id', 1)
    [class Apple, ]

And it provides built-in I/O methods allow you to dump these data in to a dictionary.

.. code-block:: python

    >>> data = Food.dump()
    >>> data
    {
        "Food": {
            "Fruit": {
                "Apple": {
                    "GreenApple": {
                        "__classname__": "GreenApple",
                        "id": 2,
                        "name": "green apple"
                    },
                    "RedApple": {
                        "__classname__": "RedApple",
                        "id": 1,
                        "name": "red apple"
                    },
                    "__classname__": "Apple",
                    "id": 1,
                    "name": "apple"
                },
                "Banana": {
                    "GreenBanana": {
                        "__classname__": "GreenBanana",
                        "id": 2,
                        "name": "green banana"
                    },
                    "YellowBanana": {
                        "__classname__": "YellowBanana",
                        "id": 1,
                        "name": "yellow banana"
                    },
                    "__classname__": "Banana",
                    "id": 2,
                    "name": "banana"
                },
                "__classname__": "Fruit",
                "id": 1,
                "name": "fruit"
            },
            "Meat": {
                "Beef": {
                    "__classname__": "Beef",
                    "id": 2,
                    "name": "beef"
                },
                "Pork": {
                    "__classname__": "Pork",
                    "id": 1,
                    "name": "pork"
                },
                "__classname__": "Meat",
                "id": 2,
                "name": "meat"
            },
            "__classname__": "Food"
        }
    }

    >>> Food = Constant.load(data)


.. _install:

Install
-------

``constant2`` is released on PyPI, so all you need is:

.. code-block:: console

	$ pip install constant2

To upgrade to latest version:

.. code-block:: console

	$ pip install --upgrade constant2