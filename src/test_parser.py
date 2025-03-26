import unittest
from markdown_parser import *

class Test_Parser(unittest.TestCase):
	def test_parser(self):
		md = "# This is an h1"
		md1 = "#This should also be an h1"
		md2 = "## This should not be h1"
		md3 = "##Neither should this"
		parsed = [extract_title(md),extract_title(md1),extract_title(md2),extract_title(md3)]
		print(parsed)
