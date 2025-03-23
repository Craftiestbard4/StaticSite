from htmlnode import *
from textnode import *
from delimiter import *

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

def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	for block in blocks:
		type = block_to_block_type(block)
		if type == BlockType.HEADING:
			level = 0
			for char in block:
				if char == "#":
					level += 1
				else:
					break
			content = block[level:].strip()
			heading_tag = f"h{level}"
			nodes = text_to_textnodes(content)
			
