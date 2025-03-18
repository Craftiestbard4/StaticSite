from htmlnode import *
from textnode import *

def txttohtml(text_node):
	match (text_node.text_type):
		case TextType.TEXT:
			html_node = LeafNode(None, text_node.text)
			return html_node
		case TextType.BOLD:
			html_node = LeafNode("b", text_node.text)
			return html_node
		case TextType.ITALIC:
			html_node = LeafNode("i", text_node.text)
			return html_node
		case TextType.CODE:
			html_node = LeafNode("code", text_node.text)
			return html_node
		case TextType.LINK:
			html_node = LeafNode("a", text_node.text, {"href": text_node.url})
			return html_node
		case TextType.IMAGE:
			html_node = LeafNode("img", "", {"src": text_node.url, "alt": text_node.alt})
			return html_node
		case _:
			raise Exception("invalid text type")
