#!/usr/bin/python3
'''testing the console'''

import unittest
import os
from models import storage
from console import MWJCommand
from unittest.mock import patch
from io import StringIO


class TestConsole(unittest.TestCase):
    """stringIO is a fake file,
       patch replaces std_out with fake file,
       mock_stdout is the file with the fake stdout contents
    """
    def setUp(self):
        '''clean state for each test'''
        self.console = MWJCommand()
        storage._FileStorage__objects.clear()

    @patch("sys.stdout", new_callable=StringIO)
    def test_create_without_arg(self, mock_stdout):
        self.console.do_create("")
        self.assertIn("** class name missing **", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_create_with_classname(self, mock_stdout):
        self.console.do_create("Lesson")
        output = mock_stdout.getvalue()
        self.assertTrue(len(output) > 0)

    @patch("sys.stdout", new_callable=StringIO)
    def test_create_with_invalid_clsname(self, mock_stdout):
        self.console.do_create("Invalid")
        self.assertIn("** class doesn't exist **", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_create_with_params(self, mock_stdout):
        self.console.do_create("Lesson name='shin'")
        output = mock_stdout.getvalue().strip()
        self.assertTrue(len(output) > 0)

        objs = storage.all()
        for key, obj in objs.items():
            if output in key:
                return obj
            continue
        self.assertEqual(obj.name, "shin")


if __name__ == "__main__":
    unittest.main()
