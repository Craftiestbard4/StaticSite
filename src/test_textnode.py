import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_eq1(self):
		node = TextNode("This is not a text node", TextType.ITALIC, "url.url.url")
		node2 = TextNode("This is a text node", TextType.ITALIC, "url.url.url")
		self.assertNotEqual(node, node2)

	def test_eq2(self):
		node = TextNode("I am a woman", TextType.NORMAL)
		node2 = TextNode("I am a woman", TextType.NORMAL, "url.url.url")
		self.assertNotEqual(node,node2)
if __name__ == "__main__":
    unittest.main()
