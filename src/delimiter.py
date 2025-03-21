import re
from textnode import *
def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []

	for old_node in old_nodes:
        # If node isn't TEXT type, just add it as-is
		if old_node.text_type != TextType.TEXT:
			new_nodes.append(old_node)
			continue

        # Handle text nodes by searching for delimiter pairs
		text = old_node.text
        # ... (search for delimiter pairs logic)
		start_index = text.find(delimiter)
		if start_index == -1: # No delimiter found
			new_nodes.append(old_node)
			continue

		end_index = text.find(delimiter, start_index + len(delimiter))
		if end_index == -1:
			raise Exception(f"No closing delimiter found for {delimiter}")

		before_text = text[:start_index]
		delimited_text = text[start_index+len(delimiter):end_index]
		after_text = text[end_index + len(delimiter):]

		if before_text:
			new_nodes.append(TextNode(before_text, TextType.TEXT))
		if delimited_text:
			new_nodes.append(TextNode(delimited_text, text_type))
		if after_text:
			temp_node = TextNode(after_text, TextType.TEXT)
			result_nodes = split_nodes_delimiter([temp_node], delimiter, text_type)
			new_nodes.extend(result_nodes)

	return new_nodes

def extract_markdown_images(text):
	return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
	return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
	new_nodes = []
	for old_node in old_nodes:
		if old_node.text_type != TextType.TEXT:
			new_nodes.append(old_node)
			continue
		images = extract_markdown_images(old_node.text)
		if not images:
			new_nodes.append(old_node)
			continue
		remaining_text = old_node.text
		for image_alt, image_url in images:
			image_markdown = f"![{image_alt}]({image_url})"
			parts = remaining_text.split(image_markdown, 1)
			if parts[0]:
				new_nodes.append(TextNode(parts[0], TextType.TEXT))
			new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
			if len(parts) > 1:
				remaining_text = parts[1]
			else:
				remaining_text = ""
		if remaining_text:
			new_nodes.append(TextNode(remaining_text, TextType.TEXT))
	return new_nodes

def split_nodes_link(old_nodes):
	new_nodes = []
	for old_node in old_nodes:
		if old_node.text_type != TextType.TEXT:
			new_nodes.append(old_node)
			continue
		links = extract_markdown_links(old_node.text)
		if not links:
			new_nodes.append(old_node)
			continue
		remaining_text = old_node.text
		for link_alt, link_url in links:
			link_markdown = f"[{link_alt}]({link_url})"
			parts = remaining_text.split(link_markdown, 1)
			if parts[0]:
				new_nodes.append(TextNode(parts[0], TextType.TEXT))
			new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
			if len(parts) > 1:
				remaining_text = parts[1]
			else:
				remaining_text = ""
		if remaining_text:
			new_nodes.append(TextNode(remaining_text, TextType.TEXT))
	return new_nodes

def text_to_textnodes(text):
	nodes = [TextNode(text, TextType.TEXT)]
	nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
	nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
	nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
	nodes = split_nodes_link(nodes)
	nodes = split_nodes_image(nodes)
	return nodes
