import unittest
from convert import *

class Test_Convert(unittest.TestCase):
	def test_text(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = txttohtml(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")

	def test_bold(self):
		node = TextNode("This is a bold node", TextType.BOLD)
		html_node = txttohtml(node)
		self.assertEqual(html_node.tag, "b")
		self.assertEqual(html_node.value, "This is a bold node")

	def test_exception(self):
		with self.assertRaises(Exception) as context:
			node = TextNode("does not matter", None)
			html_node = txttohtml(node)
		self.assertEqual(str(context.exception), "invalid text type")

	def test_img(self):
		node = TextNode("does not matter", TextType.IMAGE, "url.url.url", "alttext")
		html_node = txttohtml(node)
		self.assertEqual(html_node.value, "")
		self.assertEqual(html_node.tag, "img")
		self.assertEqual(HTMLNode.props_to_html(html_node), ' src="url.url.url" alt="alttext"')
