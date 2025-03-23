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

	def test_markdown_to_blocks(self):
		self.maxDiff=None
		md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
		blocks = markdown_to_blocks(md)
		self.assertEqual(blocks,["This is **bolded** paragraph","This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line","- This is a list\n- with items",],)

	def test_block_typer(self):
		block = "# Heading"
		block2 = "## Heading"
		block3 = "### Heading"
		block4 = "#### Heading"
		block5 = "##### Heading"
		block6 = "###### Heading"
		block7 = "####### Heading"
		block8 = "#Heading"
		results = [block_to_block_type(block),block_to_block_type(block2),block_to_block_type(block3),block_to_block_type(block4),block_to_block_type(block5),block_to_block_type(block6),block_to_block_type(block7),block_to_block_type(block8)]
		self.assertListEqual([BlockType.HEADING,BlockType.HEADING,BlockType.HEADING,BlockType.HEADING,BlockType.HEADING,BlockType.HEADING,BlockType.PARAGRAPH,BlockType.PARAGRAPH], results)

	def test_block_typer2(self):
		block = "```code```"
		block2 = "``` code ```"
		results = [block_to_block_type(block),block_to_block_type(block2)]
		self.assertListEqual([BlockType.CODE,BlockType.CODE], results)

	def test_block_typer3(self):
		block = ">Quote Quote Quote"
		block2 = "> Quote Quote Quote"
		block3 = " Not a > Quote"
		block4 = "Also > Not > a > Quote"
		results = [block_to_block_type(block),block_to_block_type(block2),block_to_block_type(block3),block_to_block_type(block4)]
		self.assertListEqual([BlockType.QUOTE,BlockType.QUOTE,BlockType.PARAGRAPH,BlockType.PARAGRAPH], results)

	def test_blodk_typer4(self):
		block = """- list\n- list\n- list\n- list"""
		block2 = "-not a list"
		block3 = "-- still not a list"
		block4 = """- still
-not
a
- list"""
		results = [block_to_block_type(block),block_to_block_type(block2),block_to_block_type(block3),block_to_block_type(block4)]
		self.assertListEqual([BlockType.UNORDERED,BlockType.PARAGRAPH,BlockType.PARAGRAPH,BlockType.PARAGRAPH], results)
	def test_block_typer5(self):
		block= "1. ordered\n2. list"
		block2= "1. not\n1. ordered\n1. list"
		block3= "1.still\n2.not\n3.ordered\n4.list"
		results = [block_to_block_type(block),block_to_block_type(block2),block_to_block_type(block3)]
		self.assertListEqual(results, [BlockType.ORDERED,BlockType.PARAGRAPH,BlockType.PARAGRAPH])
