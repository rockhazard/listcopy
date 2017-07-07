#!/usr/bin/env python3
# Python3 unit testing template


import unittest
import os
from unittest.mock import mock_open, patch, Mock
import lcp


class Test(unittest.TestCase):

    def setUp(self):
        self.testDir = os.path.expanduser('~')
        self.test_copy_files = lcp.copy_files
        self.fileList = ['TEST0.mock', 'TEST1.mock']
        self.copyList = [Mock(name='file_1'), Mock(name='file_2')]
        self.sourceFile = 'TEST.mock\nTEST.mock\n'
        self.mock = Mock()

    def tearDown(self):
        pass

    def test_number_lines(self):
        result = lcp.number_lines(self.copyList, 0)
        self.assertEqual(result, '1 >> ')

    @patch('builtins.open', mock_open(read_data='TEST0.mock\nTEST1.mock\n'))
    @patch('lcp.Path')
    def test_get_file_list(self, path):
        self.assertEqual(lcp.get_file_list(), self.fileList)
        print('Path calls: ', path.call_count)

    def test_copy_files(self):
        lcp.copy_files(self.copyList, self.testDir, fcplib=self.mock.copy2,
                       tcplib=self.mock.copy_tree)
        self.assertEqual(self.mock.copy2.call_count, 2, 'Not Equal')


'''
ASSERTS:
self.assert - base assert allowing you to write your own assertions
self.assertEqual(a, b) - check a and b are equal
self.assertNotEqual(a, b) - check a and b are not equal
self.assertIn(a, b) - check that a is in the item b
self.assertNotIn(a, b) - check that a is not in the item b
self.assertFalse(a) - check that the value of a is False
self.assertTrue(a) - check the value of a is True
self.assertIsInstance(a, TYPE) - check that a is of type "TYPE"
self.assertRaises(ERROR, a, args) - check that when a is called with 
 args that it raises ERROR
'''

if __name__ == "__main__":
    unittest.main()
