Release and Version History
===========================

0.0.14 (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.0.13 (2018-12-18)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``Constant2.BackAssign`` method, define entity mapping in a more clean way.
- add ``Constant2.ToIds``, ``Constant2.to_ids``, ``Constant2.ToIds``, ``Constant2.ToIds``, ``Constant2.ToClasses``, ``Constant2.to_instances``, ``Constant2.SubIds``, ``Constant2.sub_ids``.

**Minor Improvements**

- from 98% to 99% test converage.


0.0.12 (2018-09-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- do nothing.


0.0.11 (2018-09-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- do nothing.


0.0.10 (2018-09-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- upgrade inclueded ``superjson`` from 0.0.8 to 0.0.10
- upgrade inclueded ``inspect_mate`` from 0.0.1 to 0.0.2


0.0.9 (2018-02-05)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Features and Improvements**

- Allow inheritance.
- Require all nested class is inherit from Constant.

**Minor Improvements**

**Bugfixes**

**Miscellaneous**

- Remove code from packages that never used.


0.0.6 (2017-07-17)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**
- Fixed a bug may cause Constant.Items() and Constant.items() returns weird result.


0.0.5 (2017-07-13)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**
- Now attribute or sub classes could have mutable attributes. Modify one on this instance will not affect other instance.
- Separate the methods into two group of API (uppercase for class, lowercase for instance).

**Bugfixes**
- Fixed a import problem. Now it doesn't require to install any third party packages.


0.0.1 (2017-05-19)
~~~~~~~~~~~~~~~~~~
- First release