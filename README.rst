.. image:: https://travis-ci.org/MacHu-GWU/const-project.svg?branch=master

.. image:: https://img.shields.io/pypi/v/const.svg

.. image:: https://img.shields.io/pypi/l/const.svg

.. image:: https://img.shields.io/pypi/pyversions/const.svg


Welcome to const Documentation
==============================
If you have lots of constant value widely used across your development. A better way is to define ``Constant Variable`` rather than using the raw value. This can improve the readability.

``const`` is a library provide extensive way of managing your constant variable.

Example:

.. code-block:: python

   from const import Const


   class Food(Const):

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

           class Meat:
               id = 2
               name = "meat"


You can visit it's data or child class data in these way.


.. code-block:: python

    >>> Fruit.items() # .items() return it's    data
    [('id', 1), ('name', 'fruit')]

    >>> Fruit.keys() # .keys() return keys
    ['id', 'name']

    >>> Fruit.values() # .values() return values
    [1, 'fruit']

    >>> Fruit.to_dict() # return data in a dict
    {'id': 1, 'name': 'fruit'}

    # iterate on all nested class
    >>> Fruit.nested(sort_by='id')
    [class Apple, class Banana]

    # get first nested class that kls.id == 1
    # useful when you need reverse lookup
    >>> Fruit.get_first('id', 1)
    class Apple

    # get all child class that kls.id == 1
    >>> Fruit.get_all('id', 1)
    [class Apple, ]    


**Quick Links**
---------------
- `GitHub Homepage <https://github.com/MacHu-GWU/const-project>`_
- `Online Documentation <http://pythonhosted.org/const>`_
- `PyPI download <https://pypi.python.org/pypi/const>`_
- `Install <install_>`_
- `Issue submit and feature request <https://github.com/MacHu-GWU/const-project/issues>`_
- `API reference and source code <http://pythonhosted.org/const/py-modindex.html>`_


.. _install:

Install
-------

``const`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install const

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade const