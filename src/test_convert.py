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

	def test_paragraphs(self):
		self.maxDiff = None
		md = """This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(html,"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>")

	def test_codeblock(self):
		md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(html,"<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>")
