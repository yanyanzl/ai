#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 18:19:55 2023

@author: yanyanzhou
"""

import unittest

from coefficient import pfreturn, pfrisk

# test coefficient


def test_pfreturn():
    assert pfreturn(10, 90, 20, 30) == 10

    ...


def test_pfrisk():
    assert pfrisk(10, 90, 20, 30, 0) == 20

    ...


class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_isupper(self):
        self.assertTrue("FOO".isupper())
        self.assertFalse("Foo".isupper())

    def test_split(self):
        s = "hello world"
        self.assertEqual(s.split(), ["hello", "world"])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


"""
        self.assertIs(expr1, expr2)
        self.assertIn(member, container)
        self.assertIsNone(obj)
        self.assertIsNot(expr1, expr2)
        ...
"""


# use of setUp() and tearDown()
class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = "The widget"

    def test_default_widget_size(self):
        self.assertEqual(
            self.widget.size(), (50, 50), "incorrect default size"
        )

    def test_widget_resize(self):
        self.widget.resize(100, 150)
        self.assertEqual(
            self.widget.size(), (100, 150), "wrong size after resize"
        )

    def tearDown(self):
        self.widget.dispose()


# use subTest will run all cases even when some of them failed
class NumbersTest(unittest.TestCase):
    def test_even(self):
        """
        Test that numbers between 0 and 5 are all even.
        """
        for i in range(0, 6):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)


if __name__ == "__main__":
    unittest.main()
###########################################
"""
A testcase is created by subclassing unittest.TestCase. The three individual
tests are defined with methods whose names start with the letters test.
This naming convention informs the test runner about which methods
represent tests.

The crux of each test is a call to assertEqual() to check for an expected
result; assertTrue() or assertFalse() to verify a condition;
or assertRaises() to verify that a specific exception gets raised.
These methods are used instead of the assert statement so the test runner
can accumulate all test results and produce a report.

The setUp() and tearDown() methods allow you to define instructions
that will be executed before and after each test method.
They are covered in more detail in the section Organizing test code.


Test discovery is implemented in TestLoader.discover(), but can also
be used from the command line. The basic command-line usage is:
cd project_directory
python -m unittest discover


Tests can be numerous, and their set-up can be repetitive. Luckily, 
we can factor out set-up code by implementing a method called setUp(),
which the testing framework will automatically call for every single test 
we run

Similarly, we can provide a tearDown() method that tidies up after the 
test method has been run:
    
unittest allows you to distinguish them inside the body of a test method 
using the subTest() context manager.

assertEqual(a, b)
assertNotEqual(a, b)
assertTrue(x)
    
"""
###########################################
