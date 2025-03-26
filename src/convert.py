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
	children = []
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
			html = []
			for node in nodes:
				html.append(txttohtml(node))
			heading_node = ParentNode(heading_tag, html)
			children.append(heading_node)
		if type == BlockType.PARAGRAPH:
			text = block.replace("\n", " ").strip()
			content = text_to_textnodes(text)
			html = []
			for node in content:
				html.append(txttohtml(node))
			paragraph_node = ParentNode("p", html)
			children.append(paragraph_node)
		if type == BlockType.CODE:
			lines = block.split("\n")
			if len(lines) > 2:
				content = "\n".join(lines[1:-1]) + "\n"
			else:
				content = ""
			code_txtnode = TextNode(content, TextType.TEXT)
			htmlnode = txttohtml(code_txtnode)
			code_node = ParentNode("code", [htmlnode])
			pre_node = ParentNode("pre", [code_node])
			children.append(pre_node)
		if type == BlockType.QUOTE:
			lines = block.split("\n")
			quote = ""
			for line in lines:
				if line.startswith(">"):
					content = line[1:].strip()
					quote += content + " "
			text_nodes = text_to_textnodes(quote.strip())
			html = []
			for node in text_nodes:
				html.append(txttohtml(node))
			quote_node = ParentNode("blockquote", html)
			children.append(quote_node)
		if type == BlockType.UNORDERED:
			lines = block.split("\n")
			items = []
			for line in lines:
				if line.startswith("- "):
					item_text = line[2:].strip()
					text_nodes = text_to_textnodes(item_text)
					listed = []
					for node in text_nodes:
						listed.append(txttohtml(node))
					li_node = ParentNode("li", listed)
					items.append(li_node)
			ul_node = ParentNode("ul", items)
			children.append(ul_node)
		if type == BlockType.ORDERED:
			lines = block.split("\n")
			items = []
			for line in lines:
				if line and line[0].isdigit() and ". " in line:
					index = line.find(". ")
					if index != -1:
						item_text = line[index+2:].strip()
						text_nodes = text_to_textnodes(item_text)
						item_children = []
						for node in text_nodes:
							item_children.append(txttohtml(node))
						li_node = ParentNode("li", item_children)
						items.append(li_node)
			ol_node = ParentNode("ol", items)
			children.append(ol_node)
	parent = ParentNode("div", children)
	return parent
