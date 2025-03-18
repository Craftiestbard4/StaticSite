import unittest
from delimiter import *
from textnode import *
class TestDelimiter(unittest.TestCase):

	def test_delimiter1(self):
		nodes = [TextNode("This is a text node with a *BOLD* word", TextType.TEXT)]
		self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.BOLD), [TextNode("This is a text node with a ", TextType.TEXT), TextNode("BOLD", TextType.BOLD), TextNode(" word", TextType.TEXT)])
