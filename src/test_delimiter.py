import re
import unittest
from delimiter import *
from textnode import *
class TestDelimiter(unittest.TestCase):

	def test_delimiter1(self):
		nodes = [TextNode("This is a text node with a *BOLD* word", TextType.TEXT)]
		self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.BOLD), [TextNode("This is a text node with a ", TextType.TEXT), TextNode("BOLD", TextType.BOLD), TextNode(" word", TextType.TEXT)])

	def test_img_extracter(self):
		matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")

		self.assertListEqual([("image","https://i.imgur.com/zjjcJKZ.png")], matches)

	def test_link_extracter(self):
		text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
		self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], extract_markdown_links(text))

	def test_split_images(self):
		node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
		new_nodes = split_nodes_image([node])
		self.assertListEqual([TextNode("This is text with an ", TextType.TEXT), TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"), TextNode(" and another ", TextType.TEXT), TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")], new_nodes)

	def test_split_links(self):
		node = TextNode("This is text with a [link](https://www.google.com/) and another [link](https://www.youtube.com/)", TextType.TEXT)
		new_nodes = split_nodes_link([node])
		self.assertListEqual([TextNode("This is text with a ", TextType.TEXT), TextNode("link", TextType.LINK, "https://www.google.com/"), TextNode(" and another ", TextType.TEXT), TextNode("link", TextType.LINK, "https://www.youtube.com/")], new_nodes)

	def test_text_converter(self):
		text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		self.assertListEqual([TextNode("This is ", TextType.TEXT),TextNode("text", TextType.BOLD),TextNode(" with an ", TextType.TEXT),TextNode("italic", TextType.ITALIC),TextNode(" word and a ", TextType.TEXT),TextNode("code block", TextType.CODE),TextNode(" and an ", TextType.TEXT),TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),TextNode(" and a ", TextType.TEXT),TextNode("link", TextType.LINK, "https://boot.dev")], text_to_textnodes(text))

	def test_text_converter2(self):
		self.maxDiff=None
		text = "This is **text** with **text** in _italics_ and `code` **as well** as _more_**text** and an ![obi wan image](https://obiwan.org/)"
		self.assertListEqual([TextNode("This is ", TextType.TEXT),TextNode("text", TextType.BOLD),TextNode(" with ",TextType.TEXT),TextNode("text",TextType.BOLD),TextNode(" in ",TextType.TEXT),TextNode("italics",TextType.ITALIC),TextNode(" and ",TextType.TEXT),TextNode("code",TextType.CODE),TextNode(" ",TextType.TEXT),TextNode("as well",TextType.BOLD),TextNode(" as ",TextType.TEXT),TextNode("more",TextType.ITALIC),TextNode("text",TextType.BOLD),TextNode(" and an ",TextType.TEXT),TextNode("obi wan image", TextType.IMAGE,"https://obiwan.org/")], text_to_textnodes(text))
