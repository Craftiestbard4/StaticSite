import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
	def test_init(self):
		node = HTMLNode(None,None,None,{ "href": "https://www.google.com", "target": "_blank", })
		node1 = HTMLNode("test","test","test","test")
		self.assertNotEqual(node, node1)

	def test_props_to_html(self):
		node = HTMLNode(None,None,None,{"href": "https://www.google.com", "target": "_blank"})
		self.assertNotEqual(node.props_to_html, 'href="https://www.google.com" target="_blank"')

	def test_leafnode(self):
		node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
		self.assertEqual(node.to_html(),'<a href="https://www.google.com">Click me!</a>')

	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>")

	def test_empty_children(self):
		parent_node = ParentNode("a", [], {"href":"test.web"})
		self.assertEqual(parent_node.to_html(),'<a href="test.web"></a>')

	def test_Errors(self):
		tagless = ParentNode(None, [])
		childless = ParentNode("div", None)
		with self.assertRaises(ValueError) as context:
			tagless.to_html()
		self.assertEqual(str(context.exception), "missing tag")
		with self.assertRaises(ValueError) as context:
			childless.to_html()
		self.assertEqual(str(context.exception), "where my kids!?!?")
