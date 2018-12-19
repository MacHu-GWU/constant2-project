#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from constant2 import Constant


class Employee(Constant):
    id = None
    name = None
    department = None
    tags = list()


class EmployeeEntity(Constant):
    class E1_Alice(Employee):
        id = 1
        name = "Alice"

    class E2_Bob(Employee):
        id = 2
        name = "Bob"

    class E3_Cathy(Employee):
        id = 3
        name = "Cathy"


class Department(Constant):
    id = None
    name = None
    head = None
    employees = list()


class DepartmentEntity(Constant):
    class D1_HR(Department):
        id = 1
        name = "HR"

    class D2_IT(Department):
        id = 2
        name = "IT"


class Tag(Constant):
    id = None
    name = None
    employees = list()


class TagEntity(Constant):
    class T1_Junior(Tag):
        id = 1
        name = "Junior"

    class T2_Senior(Tag):
        id = 2
        name = "Senior"

    class T3_Python(Tag):
        id = 3
        name = "Python"

    class T4_Java(Tag):
        id = 4
        name = "Java"


# Employee and Department
EmployeeEntity.E1_Alice.department = DepartmentEntity.D1_HR
EmployeeEntity.E3_Cathy.department = DepartmentEntity.D2_IT

DepartmentEntity.BackAssign(  # back assign should be able to call multiple times
    EmployeeEntity,
    this_entity_backpopulate_field="department",
    other_entity_backpopulate_field="employees",
)
DepartmentEntity.BackAssign(
    EmployeeEntity,
    this_entity_backpopulate_field="department",
    other_entity_backpopulate_field="employees",
)
EmployeeEntity.BackAssign(
    DepartmentEntity,
    this_entity_backpopulate_field="employees",
    other_entity_backpopulate_field="department",
    is_many_to_one=True,
)
EmployeeEntity.BackAssign(
    DepartmentEntity,
    this_entity_backpopulate_field="employees",
    other_entity_backpopulate_field="department",
    is_many_to_one=True,
)

# Employee and Tag
EmployeeEntity.E1_Alice.tags = [TagEntity.T2_Senior, ]
EmployeeEntity.E2_Bob.tags = [TagEntity.T1_Junior, TagEntity.T3_Python]
EmployeeEntity.E3_Cathy.tags = [
    TagEntity.T2_Senior, TagEntity.T3_Python, TagEntity.T4_Java]

TagEntity.BackAssign(
    other_entity_klass=EmployeeEntity,
    this_entity_backpopulate_field="tags",
    other_entity_backpopulate_field="employees",
)
TagEntity.BackAssign(
    other_entity_klass=EmployeeEntity,
    this_entity_backpopulate_field="tags",
    other_entity_backpopulate_field="employees",
)
EmployeeEntity.BackAssign(
    other_entity_klass=TagEntity,
    this_entity_backpopulate_field="employees",
    other_entity_backpopulate_field="tags",
)
EmployeeEntity.BackAssign(
    other_entity_klass=TagEntity,
    this_entity_backpopulate_field="employees",
    other_entity_backpopulate_field="tags",
)


class TestDesignPattern(object):
    def test_BackAssign(self):
        # Employee vs Department
        assert EmployeeEntity.E1_Alice.department == DepartmentEntity.D1_HR
        assert EmployeeEntity.E2_Bob.department == None
        assert EmployeeEntity.E3_Cathy.department == DepartmentEntity.D2_IT

        assert DepartmentEntity.D1_HR.employees == [EmployeeEntity.E1_Alice, ]
        assert DepartmentEntity.D2_IT.employees == [EmployeeEntity.E3_Cathy]

        # Employee vs Tag
        assert EmployeeEntity.E1_Alice.tags == [TagEntity.T2_Senior, ]
        assert EmployeeEntity.E2_Bob.tags == [
            TagEntity.T1_Junior, TagEntity.T3_Python]
        assert EmployeeEntity.E3_Cathy.tags == [
            TagEntity.T2_Senior, TagEntity.T3_Python, TagEntity.T4_Java]

        assert TagEntity.T1_Junior.employees == [EmployeeEntity.E2_Bob, ]
        assert TagEntity.T2_Senior.employees == [
            EmployeeEntity.E1_Alice, EmployeeEntity.E3_Cathy]
        assert TagEntity.T3_Python.employees == [
            EmployeeEntity.E2_Bob, EmployeeEntity.E3_Cathy]
        assert TagEntity.T4_Java.employees == [EmployeeEntity.E3_Cathy, ]


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
